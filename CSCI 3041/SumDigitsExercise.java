import java.util.*;
public class SumDigitsExercise {
    // declare and define the sumDigits method here
    // public static int sumDigits ...
    public static int sumDigits(int number) {
        if (number == 0) {
            return 0;
        } else {
            return number % 10 (sumDigits / 10);
        }
    }
    public static void main (String [] args) {
        Scanner s = new Scanner(System.in);
        int input;
        String choice;
        do {
            System.out.print("\nEnter a non-negative integer: ");
            input = s.nextInt();
            if (input < 0)
            System.out.println("Please enter a non-negative integer");
            else
                System.out.println("Sum of digits in: " + input + " is: " + sumDigits(input));
            System.out.print("\n\nContinue? Enter Y or y: ");
            choice = s.next();
            System.out.println("choice: " + choice);
        } while (choice.equals("y") || choice.equals("Y"));
    }
}
