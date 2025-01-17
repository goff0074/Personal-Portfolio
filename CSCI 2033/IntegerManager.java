
import java.util.ArrayList;

public class IntegerManager {
   public void printItems(ArrayList<Integer> numsList) {
      int i;

      System.out.print("items:");

      for (i = 0; i < numsList.size(); ++i) {
         System.out.print(" " + numsList.get(i));
      }

      System.out.println();
   }

   public static void main(String[] args) {
      int i;
      IntegerManager myList = new IntegerManager();
      ArrayList<Integer> intList = new ArrayList<Integer>();

      for (i = 0; i < 5; ++i) {
         intList.add(i);
      }
      myList.printItems(intList);

      intList.add(1, 5);
      myList.printItems(intList);

      intList.remove(3);
      myList.printItems(intList);
   }
}