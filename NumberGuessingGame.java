import java.util.Random;
import java.util.Scanner;

public class NumberGuessingGame {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        Random random = new Random();

        boolean playAgain = true;

        while (playAgain) {
            int min = 1;
            int max = 100;
            int maxAttempts = 7;
            int attempts = 0;

            int secretNumber = random.nextInt(max - min + 1) + min;
            boolean guessedCorrectly = false;

            System.out.println("=================================");
            System.out.println("      NUMBER GUESSING GAME");
            System.out.println("=================================");
            System.out.println("Guess a number between" + min + " and " + max);
            System.out.println("You have " + maxAttempts + " attempts.");

            while (attempts < maxAttempts) {
                System.out.print("Enter your guess: ");
                int guess = input.nextInt();
                attempts++;

                if (guess == secretNumber) {
                    System.out.println("Congratulations! You guessed the number.");
                    System.out.println("You guessed it in " + attempts + " attempt(s).");
                    guessedCorrectly = true;
                    break;
                } else if (guess > secretNumber) {
                    System.out.println("Too high!");
                } else {
                    System.out.println("Too low!");
                }

                System.out.println("Attempts left: " + (maxAttempts - attempts));
            }

            if (!guessedCorrectly) {
                System.out.println("You lost! The correct number was: " + secretNumber);
            }

            System.out.print("Do you want to play again? (yes/no): ");
            String choice = input.next();

            playAgain = choice.equalsIgnoreCase("yes") || choice.equalsIgnoreCase("y");
        }

        System.out.println("Thanks for playing!");
        input.close();
    }
}