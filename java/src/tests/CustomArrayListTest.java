package tests;

import org.junit.Test;
import structures.CustomArrayList;

import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.assertEquals;


public class CustomArrayListTest {

    @Test
    public void TestAdd() {
        CustomArrayList<String> strings = new CustomArrayList<>(2);

        List<String> testStrings = Arrays.asList("hello", "bye", "dinner");

        for (String testString : testStrings) {
            strings.add(testString);
        }

        assertEquals(testStrings, strings);

    }
}
