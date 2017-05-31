//
// Copyright (c)2015, dblp Team (University of Trier and
// Schloss Dagstuhl - Leibniz-Zentrum fuer Informatik GmbH)
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
// (1) Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//
// (2) Redistributions in binary form must reproduce the above copyright
// notice, this list of conditions and the following disclaimer in the
// documentation and/or other materials provided with the distribution.
//
// (3) Neither the name of the dblp team nor the names of its contributors
// may be used to endorse or promote products derived from this software
// without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
// ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL DBLP TEAM BE LIABLE FOR ANY
// DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
// LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
// ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//

import java.io.IOException;
import java.util.Collection;
import java.util.Comparator;
import java.util.Map;
import java.util.TreeMap;

import org.dblp.DblpInterface;
import org.dblp.mmdb.FieldReader;
import org.dblp.mmdb.Person;
import org.dblp.mmdb.PersonName;
import org.dblp.mmdb.Publication;
import org.dblp.mmdb.datastructure.SimpleLazyCoauthorGraph;
import org.xml.sax.SAXException;


@SuppressWarnings("javadoc")
class DblpExampleParser {

    public static void main(String[] args) {

        // we need to raise entityExpansionLimit because the dblp.xml has millions of entities
        System.setProperty("entityExpansionLimit", "10000000");

        if (args.length != 1) {
            System.err.format("Usage: java %s <dblp-xml-file>\n", DblpExampleParser.class.getName());
            System.exit(0);
        }
        String dblpXmlFilename = args[0];

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

        System.out.println("finding longest name in dblp ...");
        String longestName = null;
        int longestNameLength = 0;
        for (Person pers : dblp.getPersons()) {
            for (PersonName name : pers.getNames()) {
                if (name.getName().length() > longestNameLength) {
                    longestName = name.getName();
                    longestNameLength = longestName.length();
                }
            }
        }
        System.out.format("%s (%d chars)\n\n", longestName, longestNameLength);

        System.out.println("finding most prolific author in dblp ...");
        String prolificAuthorName = null;
        int prolificAuthorCount = 0;
        for (Person pers : dblp.getPersons()) {
            int publsCount = pers.numberOfPublications();
            if (publsCount > prolificAuthorCount) {
                prolificAuthorCount = publsCount;
                prolificAuthorName = pers.getPrimaryName().getName();
            }
        }
        System.out.format("%s, %d records\n\n", prolificAuthorName, prolificAuthorCount);

        System.out.println("finding author with most coauthors in dblp ...");
        String connectedAuthorName = null;
        int connectedAuthorCount = 0;
        for (Person pers : dblp.getPersons()) {
            int coauthorCount = dblp.numberOfCoauthors(pers);
            if (coauthorCount > connectedAuthorCount) {
                connectedAuthorCount = coauthorCount;
                connectedAuthorName = pers.getPrimaryName().getName();
            }
        }
        System.out.format("%s, %d coauthors\n\n", connectedAuthorName, connectedAuthorCount);

        System.out.println("finding coauthors of Jim Gray ...");
        Person don = dblp.getPersonByName("Jim Gray");
        for (int i = 0; i < dblp.numberOfCoauthorCommunities(don); i++) {
            Collection<Person> coauthors = dblp.getCoauthorCommunity(don, i);
            System.out.format("Group %d:\n", i);
            for (Person coauthor : coauthors) {
                System.out.format("  %s\n", coauthor.getPrimaryName().getName());
            }
        }
        System.out.println();

        System.out.println("finding authors of FOCS 2010 ...");
        Comparator<Person> cmp = (Person o1,
                Person o2) -> o1.getPrimaryName().getName().compareTo(o2.getPrimaryName().getName());
        Map<Person, Integer> authors = new TreeMap<>(cmp);
        for (Publication publ : dblp.getPublications()) {
            FieldReader reader = publ.getFieldReader();
            if ("FOCS".equals(reader.valueOf("booktitle"))
                    && "2010".equals(reader.valueOf("year"))) {
                for (PersonName name : publ.getNames()) {
                    Person pers = name.getPerson();
                    if (authors.containsKey(pers)) authors.put(pers, authors.get(pers) + 1);
                    else authors.put(pers, 1);
                }
            }
        }
        for (Person author : authors.keySet())
            System.out.format("  %dx %s\n", authors.get(author), author.getPrimaryName().getName());
        System.out.println();

        System.out.println("done.");
    }
}
