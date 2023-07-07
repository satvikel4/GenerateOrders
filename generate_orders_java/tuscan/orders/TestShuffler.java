package tuscan.orders;

import java.io.File;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

public class TestShuffler {
    public static String className(final String testName) {
        return testName.substring(0, testName.lastIndexOf('.'));
    }

    private final HashMap<String, List<String>> classToMethods;
    // For tuscanInterClass
    private static int interClassRound = 0; // which class permutation to choose
    private static int interCurrentMethodRound = 0; // first class of pair
    private static int interNextMethodRound = 0; // second class of pair
    private static int i1 = 0; // current class
    private static int i2 = 1; // next class
    private static boolean isNewOrdering = false; // To change the permutation of classes

    public TestShuffler(final List<String> tests) {
        classToMethods = new HashMap<>();

        for (final String test : tests) {
            final String className = className(test);

            if (!classToMethods.containsKey(className)) {
                classToMethods.put(className, new ArrayList<>());
            }

            classToMethods.get(className).add(test);
        }
    }

    public List<String> OriginalAndTuscanOrder(int count, boolean isTuscan) {
        List<String> classes = new ArrayList<>(classToMethods.keySet());
        Collections.sort(classes);
        final List<String> fullTestOrder = new ArrayList<>();
        if (isTuscan) {
            int n = classes.size();
            int[][] res = Tuscan.generateTuscanPermutations(n);
            List<String> permClasses = new ArrayList<String>();
            for (int i = 0; i < res[count].length - 1; i++) {
                permClasses.add(classes.get(res[count][i]));
            }
            for (String className : permClasses) {
                fullTestOrder.addAll(classToMethods.get(className));
            }
        } else {
            for (String className : classes) {
                fullTestOrder.addAll(classToMethods.get(className));
            }
        }
        return fullTestOrder;
    }

    public List<String> tuscanIntraClassOrder(int round) {
        List<String> classes = new ArrayList<>(classToMethods.keySet());
        HashMap<String, int[][]> classToPermutations = new HashMap<String, int[][]>();
        Collections.sort(classes);
        final List<String> fullTestOrder = new ArrayList<>();
        int n = classes.size(); // n is number of classes
        int[][] classOrdering = Tuscan.generateTuscanPermutations(n);
        for (String className : classes) {
            int[][] methodPermuation = Tuscan.generateTuscanPermutations(classToMethods.get(className).size());
            classToPermutations.put(className, methodPermuation);
        }
        HashMap<String, List<String>> newClassToMethods = new HashMap<String, List<String>>();
        List<String> permClasses = new ArrayList<String>();
        int classRound = round;
        while ((classOrdering.length - 1) < classRound) {
            classRound -= classOrdering.length;
        }
        for (int i = 0; i < classOrdering[classRound].length - 1; i++) {
            permClasses.add(classes.get(classOrdering[classRound][i]));
        }
        for (String className : permClasses) {
            List<String> methods = classToMethods.get(className);
            List<String> permMethods = new ArrayList<String>();
            int[][] currMethodOrdering = classToPermutations.get(className);
            n = methods.size();
            int methodRound = round;
            while((currMethodOrdering.length - 1) < methodRound) {
                methodRound -= currMethodOrdering.length;
            }
            for (int i = 0; i < currMethodOrdering[methodRound].length - 1; i++) {
                permMethods.add(methods.get(currMethodOrdering[methodRound][i]));
            }
            newClassToMethods.put(className, permMethods);
        }
        for (String className : permClasses) {
            fullTestOrder.addAll(newClassToMethods.get(className));
        }
        return fullTestOrder;
    }
    
    public List<String> tuscanInterClass(int round) {
        List<String> classes = new ArrayList<>(classToMethods.keySet());
        HashMap<String, int[][]> classToPermutations = new HashMap<String, int[][]>();
        Collections.sort(classes);
        final List<String> fullTestOrder = new ArrayList<>();
        int n = classes.size(); // n is number of classes
        // If we have only one class, return the original order as a single round
        if (n == 1) {
            return OriginalAndTuscanOrder(round, false);
        }
        int[][] classOrdering = Tuscan.generateTuscanPermutations(n);

        for (String className : classes) {
            int methodSize = classToMethods.get(className).size();
            int[][] result;
            if (methodSize == 3) {
                int[][] methodPermuation = {
                    // { 0, 1, 2, 0 },
                    { 1, 0, 2, 0 },
                    { 2, 0, 1, 0 },
                    { 2, 1, 0, 0 }
                };  
                result = methodPermuation;

            } else if (methodSize == 5) {

                int[][] methodPermuation = {
                    { 0, 4, 1, 3, 2, 0 },
                    { 1, 0, 2, 4, 3, 0 },
                    { 2, 0, 3, 1, 4, 0 },
                    { 3, 4, 0, 2, 1, 0 },
                    { 4, 2, 1, 3, 0, 0 } // ,
                    // { 0, 1, 2, 3, 4, 0 }
                };
                result = methodPermuation;

            } else {

                int[][] methodPermuation = Tuscan.generateTuscanPermutations(methodSize);
                result = methodPermuation;

            }
            classToPermutations.put(className, result);
        }
        HashMap<String, List<String>> newClassToMethods = new HashMap<String, List<String>>(); // class to permutated methods
        List<String> permClasses = new ArrayList<String>();
        if (isNewOrdering) {
            // When we reach end of a permutation for classes only
            i1 = 0;
            i2 = 1;
            interNextMethodRound = 0;
            interCurrentMethodRound = 0;
            interClassRound++;
            isNewOrdering = false;
        }
        for (int i = 0; i < classOrdering[interClassRound].length - 1; i++) {
            permClasses.add(classes.get(classOrdering[interClassRound][i]));
        }
        String currentClass = permClasses.get(i1), nextClass = permClasses.get(i2);
        int currentClassMethodSize = classToMethods.get(currentClass).size();
        if (currentClassMethodSize == 3 || currentClassMethodSize == 5) {
            currentClassMethodSize++;
        }
        int nextClassMethodSize = classToMethods.get(nextClass).size();
        if (nextClassMethodSize == 3 || nextClassMethodSize == 5) {
            nextClassMethodSize++;
        }
        if (currentClassMethodSize == interCurrentMethodRound && nextClassMethodSize == (interNextMethodRound + 1)) {
            // To change the pair so we change i1 & i2
            i1++;
            i2++;
            interNextMethodRound = 0;
            interCurrentMethodRound = 0;
        }
        else if (currentClassMethodSize == (interCurrentMethodRound)) {
            // To change the *next* class methods
            interNextMethodRound++;
            interCurrentMethodRound = 0;
        }
        int[] currentClassTuscan = classToPermutations.get(currentClass)[interCurrentMethodRound];
        int[] nextClassTuscan = classToPermutations.get(nextClass)[interNextMethodRound];
        for (String className : permClasses) {
            List<String> methods = classToMethods.get(className);
            List<String> permMethods = new ArrayList<String>();
            if (className == currentClass) {
                for (int i = 0; i < currentClassTuscan.length - 1; i++) {
                    permMethods.add(methods.get(currentClassTuscan[i]));
                }
            }
            else if (className == nextClass) {
                for (int i = 0; i < nextClassTuscan.length - 1; i++) {
                    permMethods.add(methods.get(nextClassTuscan[i]));
                }
            } else {
                // We don't care about this classes permutations yet
                for (int i = 0; i < nextClassTuscan.length; i++) {
                    permMethods = methods;
                }
            }
            newClassToMethods.put(className, permMethods);
        }
        for (String className : permClasses) {
            fullTestOrder.addAll(newClassToMethods.get(className));
        }
        interCurrentMethodRound++;
        if (nextClass == permClasses.get(permClasses.size() - 1) && currentClassMethodSize == interCurrentMethodRound && nextClassMethodSize == (interNextMethodRound + 1)) {
            // if the *next class* is our last class then there is no pair so change to the next order
            isNewOrdering = true;
        }
        return fullTestOrder;
    }
}
