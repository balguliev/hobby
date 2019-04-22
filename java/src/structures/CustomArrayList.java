package structures;

import java.util.AbstractList;

public class CustomArrayList<T> extends AbstractList<T> {

    /** The items being stored. **/
    private T[] arr;
    /** The next index to be used. **/
    private int nextIn;


    /**
     * Creates a new {@code CustomArrayList} with an initial capacity of {@code initialSize}.
     *
     * @param initialSize initial capacity of this list
     * @throws IllegalArgumentException if {@code initialSize} is less than 1
     */
    public CustomArrayList(int initialSize) {
        if (initialSize < 1) {
            throw new IllegalArgumentException("initialSize must be at least 1.");
        }
        this.arr = (T[]) new Object[initialSize];
        this.nextIn = 0;
    }


    /**
     * Creates a new {@code CustomArrayList} with an initial capacity of 10.
     */
    public CustomArrayList() {
        this(10);
    }

    @Override
    public int size() {
        return nextIn;
    }

    @Override
    public T get(int index) {
        testInvalidBounds(index);
        return arr[index];
    }

    @Override
    public T set(int index, T element) {
        testInvalidBounds(index);
        T temp = arr[index];
        arr[index] = element;
        return temp;
    }

    @Override
    public boolean add(T t) {
        resizeIfNecessary();
        arr[nextIn] = t;
        nextIn++;
        return true;
    }

    private void testInvalidBounds(int index) {
        if (index < 0 || index > size()) {
            throw new IndexOutOfBoundsException();
        }
    }

    private void resizeIfNecessary() {
        if (nextIn == arr.length) {
            Object[] temp = new Object[arr.length * 2];
            System.arraycopy(arr, 0, temp, 0, size());
            arr = (T[]) temp;
        }
    }
}