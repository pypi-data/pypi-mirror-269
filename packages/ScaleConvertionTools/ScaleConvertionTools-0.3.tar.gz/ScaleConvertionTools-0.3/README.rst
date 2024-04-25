ScaleConvertionTools
-----------------------------------------------------------------

ResTransformer-based surface reflectance scale conversion tool

As a critical component of many remote sensing satellites and remote sensing model validation, image scale surface quantitative parameters are often affected by scale effects in the acquisition process, resulting in deviations in the accuracy of image scale parameters. We propose ResTransformer, a deep learning model for scale conversion of surface reflectance combined with UAV images, which can adapt to surface reflectance scale conversion scenarios with different sizes, heterogeneous sample areas and arbitrary sampling methods. The method provides a promising, highly accurate, robust approach for image element-scale surface reflectance scale conversion.

1. Processing hyperspectral images

.. code:: python

    ScaleConvertionTools
    "run this command in cmd line to start ScaleConvertionTools Window"


2. Processing uav images

.. code:: python

    ScaleConvertionTools.DataProcess.ProcessMain.Process to run ScaleConvertion by InputObject object