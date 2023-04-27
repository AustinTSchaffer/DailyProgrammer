using System;
using System.Collections.Generic;
using System.Numerics;
using Microsoft.FSharp.Collections;
using ShiftRegisters;
using ShiftRegisters.ConcreteImplementations;

namespace CSharpUsage
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("This small project demonstrates interoperability between F# and C#.");
            Console.WriteLine();

            Console.WriteLine("Creating a new shift register, which is type defined in an F# project.");
            var shiftReg = new ShiftRegister(0x0123456789ABCDEF, 64);
            Console.WriteLine($"Calling the ShiftRegister's ToString() -> '{shiftReg}'");
            Console.WriteLine();

            Console.WriteLine("Lists have some interesting interoperability.");

            var taps = ListModule.OfSeq(new List<int>() {3, 5});
            var xorLFSR = new ExclusiveOrLFSR(1, taps);

            var set = new HashSet<BigInteger>();
            var iteration = 0;
            Console.WriteLine("Looping through XOR LFSR until a duplicate value is found...");
            while (!set.Contains(xorLFSR.State))
            {
                iteration++;
                set.Add(xorLFSR.State);
                Console.WriteLine($"Iteration #{iteration}: {xorLFSR.State}");
                xorLFSR.Shift();
            }
        }
    }
}
