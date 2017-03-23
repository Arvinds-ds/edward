from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

from edward.models import RandomVariable

from edward.models import Normal, Poisson
from edward.util import copy


class test_random_variable_init_value_class(tf.test.TestCase):

  def _test_sample(self, RV, value, *args, **kwargs):
    rv = RV(*args, value=value, **kwargs)
    value_shape = rv._value.shape.as_list()
    expected_shape = (rv.get_batch_shape().as_list() +
                      rv.get_event_shape().as_list())
    self.assertEqual(value_shape, expected_shape)
    self.assertEqual(rv.dtype, rv._value.dtype)

  def _test_copy(self, RV, value, *args, **kwargs):
    rv1 = RV(*args, value=value, **kwargs)
    rv2 = copy(rv1)
    value_shape1 = rv1._value.shape.as_list()
    value_shape2 = rv2._value.shape.as_list()
    self.assertEqual(value_shape1, value_shape2)

  def test_shape_and_dtype(self):
    with self.test_session():
      self._test_sample(Normal, 2, mu=0.5, sigma=1.)
      self._test_sample(Normal, [2], mu=[0.5], sigma=[1.])
      self._test_sample(Poisson, 2, lam=0.5)

  def test_mismatch_raises(self):
    with self.test_session():
      self.assertRaises(ValueError, self._test_sample, Normal, 2,
                        mu=[0.5, 0.5], sigma=1.)
      self.assertRaises(ValueError, self._test_sample, Normal, 2,
                        mu=[0.5], sigma=[1.])
      self.assertRaises(ValueError, self._test_sample, Normal, [2],
                        mu=0.5, sigma=1.)

  def test_copy(self):
    with self.test_session():
      self._test_copy(Normal, 2, mu=0.5, sigma=1.)
      self._test_copy(Normal, [2], mu=[0.5], sigma=[1.])
      self._test_copy(Poisson, 2, lam=0.5)

if __name__ == '__main__':
  tf.test.main()