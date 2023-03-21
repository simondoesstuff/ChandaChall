using System;
using ILGPU;
using ILGPU.Runtime;
using ILGPU.Runtime.CPU;
using ILGPU.Runtime.Cuda;
using ILGPU.Runtime.OpenCL;

namespace ILGPUSample
{
    class Program
    {
        // A simple kernel that adds two vectors
        static void AddKernel(Index1D index, ArrayView<float> a, ArrayView<float> b, ArrayView<float> c)
        {
            c[index] = a[index] + b[index];
        }

        static void Main(string[] args)
        {
            // Create context and accelerator
            using var context = Context.CreateDefault();
            using var accelerator = context.CreateCPUAccelerator(0);

            // Create some sample data
            int length = 102400;
            float[] a = new float[length];
            float[] b = new float[length];
            for (int i = 0; i < length; i++)
            {
                a[i] = i;
                b[i] = 2 * i;
            }

            // Allocate buffers on the accelerator
            using var bufferA = accelerator.Allocate1D(a);
            using var bufferB = accelerator.Allocate1D(b);
            using var bufferC = accelerator.Allocate1D<float>(length);

            // Load kernel and launch it
            var kernel = accelerator.LoadAutoGroupedStreamKernel<Index1D, ArrayView<float>, ArrayView<float>, ArrayView<float>>(AddKernel);
            kernel((int)bufferA.Length, bufferA.View, bufferB.View, bufferC.View);

            // Copy result back to CPU memory and print it
            float[] c = bufferC.GetAsArray1D();
            
            Console.WriteLine("Result:");
            for (int i = 0; i < length; i++)
            {
                Console.WriteLine($"{a[i]} + {b[i]} = {c[i]}");
            }
        }
    }
}