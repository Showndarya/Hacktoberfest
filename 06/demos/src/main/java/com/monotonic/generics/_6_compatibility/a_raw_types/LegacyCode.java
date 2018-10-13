package com.monotonic.generics._6_compatibility.a_raw_types;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class LegacyCode
{
    public static void main(String[] args)
    {
        List<Object> values = new ArrayList();
        values.add("abc");
        values.add(1);
        values.add(new Object());

        List rawtype = values;
        List<String> strings = rawtype;

        for(String element : strings)
        {
            System.out.println(element);
        }

        Iterator iterator = values.iterator();
        while (iterator.hasNext())
        {
            Object element = iterator.next();
            System.out.println(element);
        }
    }
}
