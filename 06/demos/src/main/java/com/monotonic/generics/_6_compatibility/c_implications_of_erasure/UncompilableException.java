package com.monotonic.generics._6_compatibility.c_implications_of_erasure;

public class UncompilableException/*<T> */ extends Exception
{
    public static void main(String[] args)
    {
        try
        {
            throw new UncompilableException();
        }
        catch (UncompilableException/*<T>*/ e)
        {
            e.printStackTrace();
        }
    }
}
