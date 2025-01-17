import java.util.LinkedList;
import java.util.List;
import java.util.ListIterator;

public class Numbers {
   public static void main(String[] args) {
      LinkedList<Integer> numbers = new LinkedList<Integer>();
      ListIterator<Integer> numIter;
      int nextNum;

      numbers.add(4);
      numbers.add(2);
      numbers.add(3);

      numIter = numbers.listIterator();
      while (numIter.hasNext()) {
         numIter.next();
      }

      numIter.remove();
      if (numIter.hasPrevious()) {
         numIter.previous();
      }
      numIter.set(5);

      numIter = numbers.listIterator();
      while (numIter.hasNext()) {
         nextNum = numIter.next();
         System.out.println(nextNum);
      }
   }
}