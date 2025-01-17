
import java.util.ArrayList;

public class IntegersList {
   public static void main(String[] args) {
      ArrayList<Integer> userVals = new ArrayList<Integer>();
      int i;

      userVals.add(2);
      userVals.add(5);
      userVals.add(7);

      userVals.set(2, userVals.get(2) + 1);

      for (i = 0; i < userVals.size(); ++i) {
         System.out.println(userVals.get(i));
      }
   }
}