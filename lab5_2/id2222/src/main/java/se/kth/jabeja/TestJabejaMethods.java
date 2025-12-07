package se.kth.jabeja;
import se.kth.jabeja.config;

import java.util.ArrayList;
import java.util.HashMap;

public class TestJabejaMethods {
    public static void main(String[] args) {
        HashMap<Integer, Node> graph = new HashMap<>();

        // Créer quelques nœuds
        Node n1 = new Node(1, 0);
        Node n2 = new Node(2, 1);
        Node n3 = new Node(3, 0);

        // Définir les voisins
        n1.setNeighbours(new ArrayList<Integer>() {{ add(2); add(3); }});
        n2.setNeighbours(new ArrayList<Integer>() {{ add(1); add(3); }});
        n3.setNeighbours(new ArrayList<Integer>() {{ add(1); add(2); }});

        graph.put(1, n1);
        graph.put(2, n2);
        graph.put(3, n3);

        Config config = new Config(); // Assure-toi que tu as un constructeur par défaut
        Jabeja jabeja = new Jabeja(graph, config);

        // Test findPartner
        Integer[] sample = new Integer[]{2,3};
        Node partner = jabeja.findPartner(1, sample);
        System.out.println("Partner for node 1: " + partner);

        // Test sampleAndSwap
        jabeja.sampleAndSwap(1);
        System.out.println("Node 1 color after swap: " + n1.getColor());
    }
}
