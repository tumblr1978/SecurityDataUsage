//Muwei Zheng

import java.io.*;
import java.util.Collection;
import java.util.Comparator;
import java.util.Map;
import java.util.HashMap;
import java.util.HashSet;
import java.util.ArrayList;
import java.util.TreeMap;

import org.dblp.DblpInterface;
import org.dblp.mmdb.FieldReader;
import org.dblp.mmdb.Person;
import org.dblp.mmdb.PersonName;
import org.dblp.mmdb.Publication;
import org.dblp.mmdb.datastructure.SimpleLazyCoauthorGraph;
import org.xml.sax.SAXException;



@SuppressWarnings("javadoc")
class DblpPaperListParser {
    //Initialize static variables;
    //HashMap outPapers -> {"conference":["PaperName","url","conf","year"]}
    static HashMap<String, ArrayList<String[]>> confs = new HashMap<String, ArrayList<String[]>> ();

    //helper method to open conferenceList file.
    static void initMap(String fileName, String year){
        File file = new File(fileName);
        try{
            BufferedReader reader = new BufferedReader(new FileReader(file));
            String conf;
            reader.readLine();
            while ((conf = reader.readLine()) != null){
                conf = conf.split(",")[1];
                confs.put(conf, new ArrayList<String[]>());
            }
            reader.close();
        }catch(IOException e){
            System.out.println("Cannot obtain the list of conferences. System exits.");
            System.exit(1);
        }
    }

    //helper method to write output to a new file called papers.csv
    static void writePapers(HashMap<String, ArrayList<String[]>> confs, String year){
        String filename = "papers"+year+".csv";
        try{
            PrintWriter writer = new PrintWriter("./data/"+filename);
            writer.println("Paper, URL, Conference, Year");
            for (ArrayList<String[]> conf : confs.values()){
                for (String[] paper : conf){
                    writer.println(String.join(",",paper));
                }
            }
            writer.close();
        }catch(IOException e){
            System.out.println("Cannot reach the output file");
            System.out.println(e);
            System.exit(1);
        }
    }

    public static void main(String[] args) {

        // we need to raise entityExpansionLimit because the dblp.xml has millions of entities
        System.setProperty("entityExpansionLimit", "10000000");

        if (args.length != 3) {
            System.err.format("Usage: java %s <dblp-xml-file>\n", DblpPaperListParser.class.getName());
            System.exit(0);
        }
        String dblpXmlFilename = args[0];
        String fileName = args[1];
        String year = args[2];

        System.out.println("building the dblp main memory DB ...");
        DblpInterface dblp;
        try {
            dblp = new SimpleLazyCoauthorGraph(dblpXmlFilename);
        }
        catch (final IOException ex) {
            System.err.println("cannot read dblp XML: " + ex.getMessage());
            return;
        }
        catch (final SAXException ex) {
            System.err.println("cannot parse XML: " + ex.getMessage());
            return;
        }
        System.out.format("MMDB ready: %d publs, %d pers\n\n", dblp.numberOfPublications(), dblp.numberOfPersons());
        

        initMap(fileName, year);
        HashSet<String> mapKeys = new HashSet<String>(confs.keySet());


        System.out.println("Reading data...");
        for (Publication publ : dblp.getPublications()) {
            FieldReader reader = publ.getFieldReader();
            
            String conf = reader.valueOf("crossref");
            if (conf == null) continue;
            String[] confAttr = conf.split("/");
            if (confAttr[2].length()> 4) conf = confAttr[1] + confAttr[2].substring(4);
            else conf = confAttr[1];

            if (mapKeys.contains(conf) && year.equals(reader.valueOf("year"))) {
                int pages = 1;
                if (reader.valueOf("pages") != null){
                    String[] pageRange = reader.valueOf("pages").split("-");
                    if (pageRange.length >1)
                        pages= Integer.parseInt(pageRange[1]) - Integer.parseInt(pageRange[0]);
                }else pages = 4;

                if (pages >3){
                    String[] paper = new String[4];
                    paper[0] = "\""+reader.valueOf("title")+"\"";
                    paper[1] = reader.valueOf("ee");
                    paper[2] = conf;
                    paper[3] = year;
                    confs.get(conf).add(paper);
                }
            }
        }


        writePapers(confs, year);
        
        System.out.println("done");
    }
}
