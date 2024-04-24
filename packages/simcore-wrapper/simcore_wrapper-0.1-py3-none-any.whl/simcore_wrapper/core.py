import jpype
import jpype.imports
# from jpype.types import *
import numpy as np


# Start the JVM
def start_jvm(jar_path):
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=[jar_path])
        print('JVM is started')


# Example class to wrap Kotlin functionality
class SimCore:
    def __init__(self, jar_path):
        start_jvm(jar_path)

    def perform_action(self, arg):
        # Import your Kotlin classes using jpype
        from com.jetbrains.ksim.sandbox.forpy.example.FunctionsKt import get2DDoubleArray
        # Example of calling a method from the Kotlin class
        print("\nConvert Kotlin 2D Array to np.array:")
        print("-------------------------------------------------------------------------------")
        kotlin_2d_array = get2DDoubleArray(5, 5, 3.14)
        print(f"kotlin_2d_array = {kotlin_2d_array}")
        mp_2d_array = np.array(kotlin_2d_array)
        print(f"mp_2d_array.shape = {mp_2d_array.shape}")
        print(f"mp_2d_array = {mp_2d_array}")
