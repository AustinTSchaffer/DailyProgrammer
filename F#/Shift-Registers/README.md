# Linear Feedback Shift Register (LFSR)

This repository contains a software implementation of a Linear Feedback Shift 
Register (LFSR) using F#.

A shift register is a hardware structure in a digital circuit that consists of 
a series of registers. In a typical shift register, all of the stored bits are 
shifted in one direction, by one register, on each clock tick. In a typical 
shift register, the first register in the series comes from an arbitrary 
source, while bits that reach the end of the register fall off and are not 
recycled. 

An LSFR are similar to regular shift registers, except the input is a "linear 
function of its previous state". LFSRs can be built out of regular shift 
registers, as long as the state of internal bits is queryable. The most common 
LFSRs appear to use XOR as the linear function, where a predetermined 
combination of state registered are multiXORed together in order to generate 
an input. 

The objective of this software package is to build a software implementation 
of an LFSR, providing options for the length and the feedback function. 

## Dependencies

- F# 4.1.x
- F# .NET SDK 1.0.x
- .NET Standard 1.6
- .NET Standard 1.6
- .NET Core 1.1