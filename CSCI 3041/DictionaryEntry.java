import java.util.Comparator;

public class DictionaryEntry implements Comparable<DictionaryEntry> {

    // instance variables
    private String wordOrPhrase;
    private String definition;

    // constructors
    public DictionaryEntry() {}

    public DictionaryEntry(String wop, String def) {
        this.wordOrPhrase = wop;
        this.definition = def;
    }

    // getters and setters
    public String getWordOrPhrase() {
        return wordOrPhrase;
    }

    public void setWordOrPhrase(String wordOrPhrase) {
        this.wordOrPhrase = wordOrPhrase;
    }

    public String getDefinition() {
        return definition;
    }

    public void setDefinition(String definition) {
        this.definition = definition;
    }

    // returns a String array with the wordOrPhrase at location zero and definition
    // at location 1
    public String[] getData() {
        return new String[]{wordOrPhrase, definition};
    }

    // accepts a String array with the wordOrPhrase at location zero and the definition
    // of the wordOrPhrase at location 1 and sets the variables accordingly
    public void setData(String[] data) {
        if (data.length == 2) {
            this.wordOrPhrase = data[0];
            this.definition = data[1];
        }
    }

    // Define a Comparator method that can be used to sort an ArrayList of Nodes in Lexically
    // Ascending order - that is, from A to Z, according to the wordOrPhrase
    // Note that you must keep the exact method signature provided here
    public static Comparator<DictionaryEntry> lexicalComparator = Comparator.comparing(DictionaryEntry::getWordOrPhrase);

    @Override
    public int compareTo(DictionaryEntry o) {
        return this.wordOrPhrase.compareTo(o.getWordOrPhrase());
    }
}
