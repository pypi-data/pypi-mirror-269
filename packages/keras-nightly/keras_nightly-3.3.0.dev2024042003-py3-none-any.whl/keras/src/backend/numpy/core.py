import numpy as np

from keras.src import tree
from keras.src.backend.common import KerasVariable
from keras.src.backend.common import standardize_dtype
from keras.src.backend.common.dtypes import result_type
from keras.src.backend.common.keras_tensor import KerasTensor
from keras.src.backend.common.stateless_scope import StatelessScope

SUPPORTS_SPARSE_TENSORS = False


class Variable(KerasVariable):
    def _initialize(self, value):
        self._value = np.array(value, dtype=self._dtype)

    def _direct_assign(self, value):
        self._value = np.array(value, dtype=self._dtype)

    def _convert_to_tensor(self, value, dtype=None):
        return convert_to_tensor(value, dtype=dtype)

    # Overload native accessor.
    def __array__(self):
        return self.value


def convert_to_tensor(x, dtype=None, sparse=None):
    if sparse:
        raise ValueError("`sparse=True` is not supported with numpy backend")
    if dtype is not None:
        dtype = standardize_dtype(dtype)
    if isinstance(x, Variable):
        if dtype and dtype != x.dtype:
            return x.value.astype(dtype)
        return x.value
    if not is_tensor(x) and standardize_dtype(dtype) == "bfloat16":
        # Can't create bfloat16 arrays on the fly (e.g. from a h5 Dataset).
        # Instead we convert "as is" (to stored dtype) and cast.
        return np.asarray(x).astype(dtype)
    if dtype is None:
        dtype = result_type(
            *[getattr(item, "dtype", type(item)) for item in tree.flatten(x)]
        )
    return np.array(x, dtype=dtype)


def convert_to_numpy(x):
    return np.array(x)


def is_tensor(x):
    if isinstance(x, (np.generic, np.ndarray)):
        return True
    return False


def shape(x):
    return x.shape


def cast(x, dtype):
    return convert_to_tensor(x, dtype=dtype)


def cond(pred, true_fn, false_fn):
    if pred:
        return true_fn()
    return false_fn()


def vectorized_map(function, elements):
    if not isinstance(elements, (list, tuple)):
        return np.stack([function(x) for x in elements])
    else:
        batch_size = elements[0].shape[0]
        output_store = []
        for index in range(batch_size):
            output_store.append(function([x[index] for x in elements]))
        return np.stack(output_store)


# Shape / dtype inference util
def compute_output_spec(fn, *args, **kwargs):
    with StatelessScope():

        def has_none_shape(x):
            if isinstance(x, KerasTensor):
                return None in x.shape
            return False

        none_in_shape = any(map(has_none_shape, tree.flatten((args, kwargs))))

        def convert_keras_tensor_to_numpy(x, fill_value=None):
            if isinstance(x, KerasTensor):
                shape = list(x.shape)
                if fill_value:
                    for i, e in enumerate(shape):
                        if e is None:
                            shape[i] = fill_value
                return np.empty(
                    shape=shape,
                    dtype=x.dtype,
                )
            return x

        args_1, kwargs_1 = tree.map_structure(
            lambda x: convert_keras_tensor_to_numpy(x, fill_value=83),
            (args, kwargs),
        )
        outputs_1 = fn(*args_1, **kwargs_1)

        outputs = outputs_1

        if none_in_shape:
            args_2, kwargs_2 = tree.map_structure(
                lambda x: convert_keras_tensor_to_numpy(x, fill_value=89),
                (args, kwargs),
            )
            outputs_2 = fn(*args_2, **kwargs_2)

            flat_out_1 = tree.flatten(outputs_1)
            flat_out_2 = tree.flatten(outputs_2)

            flat_out = []
            for x1, x2 in zip(flat_out_1, flat_out_2):
                shape = list(x1.shape)
                for i, e in enumerate(x2.shape):
                    if e != shape[i]:
                        shape[i] = None
                flat_out.append(KerasTensor(shape, standardize_dtype(x1.dtype)))
            outputs = tree.pack_sequence_as(outputs_1, flat_out)

        def convert_numpy_to_keras_tensor(x):
            if is_tensor(x):
                return KerasTensor(x.shape, standardize_dtype(x.dtype))
            return x

        output_spec = tree.map_structure(convert_numpy_to_keras_tensor, outputs)
    return output_spec


def scatter(indices, values, shape):
    indices = convert_to_tensor(indices)
    values = convert_to_tensor(values)
    zeros = np.zeros(shape, dtype=values.dtype)

    index_length = indices.shape[-1]
    value_shape = shape[index_length:]
    indices = np.reshape(indices, [-1, index_length])
    values = np.reshape(values, [-1] + list(value_shape))

    for i in range(indices.shape[0]):
        index = indices[i]
        zeros[tuple(index)] += values[i]
    return zeros


def scatter_update(inputs, indices, updates):
    indices = np.array(indices)
    indices = np.transpose(indices)
    inputs[tuple(indices)] = updates
    return inputs


def slice(inputs, start_indices, lengths):
    # Validate inputs
    assert len(start_indices) == len(lengths)

    # Generate list of indices arrays for each dimension
    indices = [
        np.arange(start, start + length)
        for start, length in zip(start_indices, lengths)
    ]

    # Use np.ix_ to create a multidimensional index array
    mesh = np.ix_(*indices)

    return inputs[mesh]


def slice_update(inputs, start_indices, updates):
    # Generate list of indices arrays for each dimension
    indices = [
        np.arange(start, start + length)
        for start, length in zip(start_indices, updates.shape)
    ]

    # Use np.ix_ to create a multidimensional index array
    mesh = np.ix_(*indices)
    inputs[mesh] = updates
    return inputs


def while_loop(
    cond,
    body,
    loop_vars,
    maximum_iterations=None,
):
    current_iter = 0
    iteration_check = (
        lambda iter: maximum_iterations is None or iter < maximum_iterations
    )
    is_tuple = isinstance(loop_vars, (tuple, list))
    loop_vars = tuple(loop_vars) if is_tuple else (loop_vars,)
    loop_vars = tree.map_structure(convert_to_tensor, loop_vars)
    while cond(*loop_vars) and iteration_check(current_iter):
        loop_vars = body(*loop_vars)
        if not isinstance(loop_vars, (list, tuple)):
            loop_vars = (loop_vars,)
        loop_vars = tuple(loop_vars)
        current_iter += 1
    return loop_vars if is_tuple else loop_vars[0]


def fori_loop(lower, upper, body_fun, init_val):
    val = init_val
    for i in range(lower, upper):
        val = body_fun(i, val)
    return val


def stop_gradient(x):
    return x


def unstack(x, num=None, axis=0):
    x = np.moveaxis(x, axis, 0)
    return [x[i] for i in range(x.shape[0])]


def custom_gradient(fun):
    raise NotImplementedError(
        "`custom_gradient` is not supported with numpy backend"
    )
