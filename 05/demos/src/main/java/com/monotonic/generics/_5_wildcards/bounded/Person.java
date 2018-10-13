package com.monotonic.generics._5_wildcards.bounded;

import java.util.Objects;

public class Person
{
    private final String name;
    private final int age;

    public Person(String name, int age)
    {
        Objects.requireNonNull(name);

        this.name = name;
        this.age = age;
    }

    public int getAge()
    {
        return age;
    }

    public String getName()
    {
        return name;
    }

    @Override
    public boolean equals(Object o)
    {
        if (o == null || getClass() != o.getClass()) return false;

        Person person = (Person) o;

        return age == person.age
            && name.equals(person.name);
    }

    @Override
    public int hashCode()
    {
        int result = name.hashCode();
        result = 31 * result + age;
        return result;
    }

    @Override
    public String toString()
    {
        return "Person{" +
            "name='" + name + '\'' +
            ", age=" + age +
            '}';
    }
}
