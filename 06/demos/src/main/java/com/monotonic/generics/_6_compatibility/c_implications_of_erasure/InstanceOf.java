package com.monotonic.generics._6_compatibility.c_implications_of_erasure;

public class InstanceOf<T>
{
    public boolean equals(Object o)
    {
        // Banned
        if (o instanceof InstanceOf/*<T>*/)
        {
            return true;
        }

        return false;
    }
}
