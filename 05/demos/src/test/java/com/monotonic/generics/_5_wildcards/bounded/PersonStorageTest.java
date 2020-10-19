package com.monotonic.generics._5_wildcards.bounded;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import static java.util.Arrays.asList;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;

public class PersonStorageTest
{
    private Partner donDraper = new Partner("Don Draper", 89);
    private Partner bertCooper = new Partner("Bert Cooper", 100);
    private Employee peggyOlson = new Employee("Peggy Olson", 65);

    private File file;
    private PersonSaver saver;
    private PersonLoader loader;

    @Test
    public void cannotLoadFromEmptyFile() throws Exception
    {
        PersonLoader loader = new PersonLoader(file);

        assertNull(loader.load());
    }

    @Test
    public void savesAndLoadsPerson() throws Exception
    {
        PersonSaver saver = new PersonSaver(file);
        PersonLoader loader = new PersonLoader(file);

        saver.save(donDraper);

        assertEquals(donDraper, loader.load());
    }

    @Test
    public void savesAndLoadsTwoPeople() throws Exception
    {
        saver.save(donDraper);
        saver.save(peggyOlson);

        assertEquals(donDraper, loader.load());
        assertEquals(peggyOlson, loader.load());
    }

    @Test
    public void savesArraysOfPeople() throws Exception
    {
        /*Employee[] employees = new Employee[2];
        Person[] people = employees;*/
        Partner[] people = new Partner[2];
        people[0] = donDraper;
        people[1] = bertCooper;

        saver.saveAll(people);

        assertEquals(donDraper, loader.load());
        assertEquals(bertCooper, loader.load());
    }

    @Test
    public void savesListsOfPeople() throws Exception
    {
        List<Partner> people = new ArrayList<>();
        people.add(donDraper);
        people.add(bertCooper);

        saver.saveAll(people);

        assertEquals(donDraper, loader.load());
        assertEquals(bertCooper, loader.load());
    }

    @Test
    public void loadsListsOfPeople() throws Exception
    {
        saver.save(donDraper);
        saver.save(bertCooper);

        List<Object> people = new ArrayList<>();
        loader.loadAll(people);


        assertEquals(asList(donDraper, bertCooper), people);
    }

    @Before
    public void setUp() throws Exception
    {
        file = File.createTempFile("tmp", "people");
        saver = new PersonSaver(file);
        loader = new PersonLoader(file);
    }

    @After
    public void tearDown()
    {
        if (file.exists())
        {
            file.delete();
        }
    }
}
