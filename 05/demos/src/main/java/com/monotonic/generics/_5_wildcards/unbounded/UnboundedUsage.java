package com.monotonic.generics._5_wildcards.unbounded;

import com.monotonic.generics._5_wildcards.bounded.Person;

import java.util.ArrayList;
import java.util.List;

public class UnboundedUsage
{
    public static void main(String[] args) throws ClassNotFoundException
    {
        List<Object> objects = new ArrayList<>();
        objects.add(new Object());
        objects.add(new Person("Don Draper", 89));
        System.out.println(objects);

        // Its only safe to add null to a List<?>
        List<?> wildcards = new ArrayList<>();
        wildcards.add(null);
        System.out.println(wildcards);
    }

}
