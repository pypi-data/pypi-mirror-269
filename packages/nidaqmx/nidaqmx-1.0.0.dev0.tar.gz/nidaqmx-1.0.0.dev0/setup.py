# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'generated'}

packages = \
['nidaqmx',
 'nidaqmx._stubs',
 'nidaqmx.system',
 'nidaqmx.system._collections',
 'nidaqmx.system._watchdog_modules',
 'nidaqmx.system.storage',
 'nidaqmx.task',
 'nidaqmx.task.channels',
 'nidaqmx.task.collections',
 'nidaqmx.task.triggering']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.0',
 'deprecation>=2.1',
 'hightime>=0.2.2,<0.3.0',
 'python-decouple>=3.8',
 'tzlocal>=5.0,<6.0']

extras_require = \
{':python_version >= "3.12" and python_version < "3.13"': ['numpy>=1.26'],
 ':python_version >= "3.8" and python_version < "3.12"': ['numpy>=1.22'],
 'docs': ['Sphinx>=5.0', 'sphinx_rtd_theme>=1.0'],
 'grpc': ['grpcio>=1.49.0,<2.0', 'protobuf>=4.21,<5.0']}

entry_points = \
{'console_scripts': ['nidaqmx = nidaqmx.__main__:main']}

setup_kwargs = {
    'name': 'nidaqmx',
    'version': '1.0.0.dev0',
    'description': 'NI-DAQmx Python API',
    'long_description': '===========  =================================================================================================================================\nInfo         Contains a Python API for interacting with NI-DAQmx. See `GitHub <https://github.com/ni/nidaqmx-python/>`_ for the latest source.\nAuthor       National Instruments\n===========  =================================================================================================================================\n\nAbout\n=====\n\nThe **nidaqmx** package contains an API (Application Programming Interface)\nfor interacting with the NI-DAQmx driver. The package is implemented in Python.\nThe package is implemented as a complex, \nhighly object-oriented wrapper around the NI-DAQmx C API using the \n`ctypes <https://docs.python.org/2/library/ctypes.html>`_ Python library.\n\n**nidaqmx** supports all versions of the NI-DAQmx driver that ships with the C\nAPI. The C API is included in any version of the driver that supports it. The\n**nidaqmx** package does not require installation of the C header files.\n\nSome functions in the **nidaqmx** package may be unavailable with earlier \nversions of the NI-DAQmx driver. Visit the \n`ni.com/downloads <http://www.ni.com/downloads/>`_ to upgrade your version of \nNI-DAQmx.\n\n**nidaqmx** supports Windows and Linux operating systems where the NI-DAQmx\ndriver is supported. Refer to\n`NI Hardware and Operating System Compatibility <https://www.ni.com/r/hw-support>`_\nfor which versions of the driver support your hardware on a given operating\nsystem.\n\n**nidaqmx** supports CPython 3.8+ and PyPy3.\n\nInstallation\n============\n\nRunning **nidaqmx** requires NI-DAQmx to be installed. Visit\n`ni.com/downloads <http://www.ni.com/downloads/>`_ to download the latest\nversion of NI-DAQmx. None of the recommended **Additional items** are required\nfor **nidaqmx** to function, and they can be removed to minimize installation\nsize. It is recommended you continue to install the **NI Certificates** package\nto allow your Operating System to trust NI built binaries, improving your\nsoftware and hardware installation experience.\n\n**nidaqmx** can be installed with `pip <http://pypi.python.org/pypi/pip>`_::\n\n  $ python -m pip install nidaqmx\n\nSimilar Packages\n================\n\nThere are similar packages available that also provide NI-DAQmx functionality in\nPython:\n\n- `daqmx <https://pypi.org/project/daqmx/>`_\n  (`slightlynybbled/daqmx on GitHub <https://github.com/slightlynybbled/daqmx>`_)\n  provides an abstraction of NI-DAQmx in the ``ni`` module.\n\n- PyLibNIDAQmx (`pearu/pylibnidaqmx on GitHub <https://github.com/pearu/pylibnidaqmx>`_)\n  provides an abstraction of NI-DAQmx in the ``nidaqmx`` module, which collides\n  with this package\'s module name.\n\n.. _usage-section:\n\nUsage\n=====\nThe following is a basic example of using an **nidaqmx.task.Task** object. \nThis example illustrates how the single, dynamic **nidaqmx.task.Task.read** \nmethod returns the appropriate data type.\n\n.. code-block:: python\n\n  >>> import nidaqmx\n  >>> with nidaqmx.Task() as task:\n  ...     task.ai_channels.add_ai_voltage_chan("Dev1/ai0")\n  ...     task.read()\n  ...\n  -0.07476920729381246\n  >>> with nidaqmx.Task() as task:\n  ...     task.ai_channels.add_ai_voltage_chan("Dev1/ai0")\n  ...     task.read(number_of_samples_per_channel=2)\n  ...\n  [0.26001373311970705, 0.37796597238117036]\n  >>> from nidaqmx.constants import LineGrouping\n  >>> with nidaqmx.Task() as task:\n  ...     task.di_channels.add_di_chan(\n  ...         "cDAQ2Mod4/port0/line0:1", line_grouping=LineGrouping.CHAN_PER_LINE)\n  ...     task.read(number_of_samples_per_channel=2)\n  ...\n  [[False, True], [True, True]]\n\nA single, dynamic **nidaqmx.task.Task.write** method also exists.\n\n.. code-block:: python\n\n  >>> import nidaqmx\n  >>> from nidaqmx.types import CtrTime\n  >>> with nidaqmx.Task() as task:\n  ...     task.co_channels.add_co_pulse_chan_time("Dev1/ctr0")\n  ...     sample = CtrTime(high_time=0.001, low_time=0.001)\n  ...     task.write(sample)\n  ...\n  1\n  >>> with nidaqmx.Task() as task:\n  ...     task.ao_channels.add_ao_voltage_chan("Dev1/ao0")\n  ...     task.write([1.1, 2.2, 3.3, 4.4, 5.5], auto_start=True)\n  ...\n  5\n\nConsider using the **nidaqmx.stream_readers** and **nidaqmx.stream_writers**\nclasses to increase the performance of your application, which accept pre-allocated\nNumPy arrays.\n\nFollowing is an example of using an **nidaqmx.system.System** object.\n\n.. code-block:: python\n\n  >>> import nidaqmx.system\n  >>> system = nidaqmx.system.System.local()\n  >>> system.driver_version\n  DriverVersion(major_version=16L, minor_version=0L, update_version=0L)\n  >>> for device in system.devices:\n  ...     print(device)\n  ...\n  Device(name=Dev1)\n  Device(name=Dev2)\n  Device(name=cDAQ1)\n  >>> import collections\n  >>> isinstance(system.devices, collections.Sequence)\n  True\n  >>> device = system.devices[\'Dev1\']\n  >>> device == nidaqmx.system.Device(\'Dev1\')\n  True\n  >>> isinstance(device.ai_physical_chans, collections.Sequence)\n  True\n  >>> phys_chan = device.ai_physical_chans[\'ai0\']\n  >>> phys_chan\n  PhysicalChannel(name=Dev1/ai0)\n  >>> phys_chan == nidaqmx.system.PhysicalChannel(\'Dev1/ai0\')\n  True\n  >>> phys_chan.ai_term_cfgs\n  [<TerminalConfiguration.RSE: 10083>, <TerminalConfiguration.NRSE: 10078>, <TerminalConfiguration.DIFFERENTIAL: 10106>]\n  >>> from enum import Enum\n  >>> isinstance(phys_chan.ai_term_cfgs[0], Enum)\n  True\n\nBugs / Feature Requests\n=======================\n\nTo report a bug or submit a feature request, please use the \n`GitHub issues page <https://github.com/ni/nidaqmx-python/issues>`_.\n\nInformation to Include When Asking for Help\n-------------------------------------------\n\nPlease include **all** of the following information when opening an issue:\n\n- Detailed steps on how to reproduce the problem and full traceback, if \n  applicable.\n- The python version used::\n\n  $ python -c "import sys; print(sys.version)"\n\n- The versions of the **nidaqmx** and numpy packages used::\n\n  $ python -m pip list\n\n- The version of the NI-DAQmx driver used. Follow \n  `this KB article <http://digital.ni.com/express.nsf/bycode/ex8amn>`_ \n  to determine the version of NI-DAQmx you have installed.\n- The operating system and version, for example Windows 7, CentOS 7.2, ...\n\nDocumentation\n=============\n\nDocumentation is available `here <http://nidaqmx-python.readthedocs.io>`_.\n\nAdditional Documentation\n========================\n\nRefer to the `NI-DAQmx Help <http://digital.ni.com/express.nsf/bycode/exagg4>`_ \nfor API-agnostic information about NI-DAQmx or measurement concepts.\n\nNI-DAQmx Help installs only with the full version of NI-DAQmx.\n\nLicense\n=======\n\n**nidaqmx** is licensed under an MIT-style license (see\n`LICENSE <https://github.com/ni/nidaqmx-python/blob/master/LICENSE>`_).\nOther incorporated projects may be licensed under different licenses. All\nlicenses allow for non-commercial and commercial use.\n\n**gRPC Features**\nFor driver APIs that support it, passing a GrpcSessionOptions instance as a\nparameter is subject to the NI General Purpose EULA\n(`see NILICENSE <https://github.com/ni/nidaqmx-python/blob/master/NILICENSE>`_).',
    'author': 'NI',
    'author_email': 'opensource@ni.com',
    'maintainer': 'Zach Hindes',
    'maintainer_email': 'zach.hindes@ni.com',
    'url': 'https://github.com/ni/nidaqmx-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
