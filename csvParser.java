//import java.io.*;
import java.util.*;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.concurrent.atomic.AtomicInteger;


/**
 *
 * @author Juan Andres Nunez
 * @version 1.0
 * @since 2024-11-16
 */
public class csvParser {
    public static void main(String[] args) {
        
        // Verificar que se proporcionó el argumento db-path
        if (args.length == 0) {
            System.err.println("Error: Se requiere el argumento db-path");
            System.err.println("Uso: java csvParser <db-path>");
            System.err.println("Ejemplo: java csvParser social_network-csv_basic-sf0.1");
            System.exit(1);
        }
        
        // Obtener el argumento db-path
        String dbPath = args[0];
        
        // Construir la ruta completa
        String basePath = System.getProperty("user.dir") + File.separator + dbPath;
        
        System.out.println("Usando ruta de base de datos: " + basePath);



        String resultadosFolder = System.getProperty("user.dir") + File.separator + "resultados" + File.separator;
        String resultadosMain = System.getProperty("user.dir");
        Map<String, String> nodeFiles = new HashMap<>();
        nodeFiles.put("person", basePath + File.separator + "dynamic" + File.separator + "person_0_0.csv");
        nodeFiles.put("comment", basePath + File.separator + "dynamic" + File.separator + "comment_0_0.csv");
        nodeFiles.put("place", basePath + File.separator + "static" + File.separator + "place_0_0.csv");
        nodeFiles.put("organisation", basePath + File.separator + "static" + File.separator + "organisation_0_0.csv");
        nodeFiles.put("forum", basePath + File.separator + "dynamic" + File.separator + "forum_0_0.csv");
        nodeFiles.put("post", basePath + File.separator + "dynamic" + File.separator + "post_0_0.csv");
        nodeFiles.put("tag", basePath + File.separator + "static" + File.separator + "tag_0_0.csv");
        nodeFiles.put("tagClass", basePath + File.separator + "static" + File.separator + "tagclass_0_0.csv");

        Map<String, String> prefijos = new HashMap<>();
        prefijos.put("person", "p");
        prefijos.put("comment", "m"); 
        prefijos.put("post", "m");     
        prefijos.put("place", "pL");
        prefijos.put("organisation", "o");
        prefijos.put("forum", "f");
        prefijos.put("tag", "t");
        prefijos.put("tagClass", "tc");
        
        List<Elemento> prefijosPorRelacion = new ArrayList<>();
        prefijosPorRelacion.add(new Elemento("commentCreator", new String[]{"m", "p"}));
        prefijosPorRelacion.add(new Elemento("personLikes", new String[]{"p", "m"}));
        prefijosPorRelacion.add(new Elemento("commentReplyOfComment", new String[]{"m", "m"}));
        prefijosPorRelacion.add(new Elemento("postCreator", new String[]{"m", "p"}));
        prefijosPorRelacion.add(new Elemento("forumPost", new String[]{"f", "m"}));
        prefijosPorRelacion.add(new Elemento("forumMember", new String[]{"f", "p"}));
        prefijosPorRelacion.add(new Elemento("forumModerator", new String[]{"f", "p"}));
        prefijosPorRelacion.add(new Elemento("personLikesPost", new String[]{"p", "m"})); 
        prefijosPorRelacion.add(new Elemento("personHasInterest", new String[]{"p", "t"}));
        prefijosPorRelacion.add(new Elemento("forumHasTag", new String[]{"f", "t"}));
        prefijosPorRelacion.add(new Elemento("postHasTag", new String[]{"m", "t"}));
        prefijosPorRelacion.add(new Elemento("commentHasTag", new String[]{"m", "t"}));
        prefijosPorRelacion.add(new Elemento("tagIsSubClassOf", new String[]{"tc", "tc"}));
        prefijosPorRelacion.add(new Elemento("commentIsLocatedIn", new String[]{"m", "pL"})); 
        prefijosPorRelacion.add(new Elemento("personIsLocatedIn", new String[]{"p", "pL"}));  
        prefijosPorRelacion.add(new Elemento("personStudyAt", new String[]{"p", "o"}));
        prefijosPorRelacion.add(new Elemento("personWorkAt", new String[]{"p", "o"}));
        prefijosPorRelacion.add(new Elemento("placeIsPartOf", new String[]{"pL", "pL"}));  
        prefijosPorRelacion.add(new Elemento("tagHasType", new String[]{"t", "tc"}));  
        prefijosPorRelacion.add(new Elemento("commentReplyOfPost", new String[]{"m", "m"}));
        prefijosPorRelacion.add(new Elemento("organisationIsLocatedIn", new String[]{"o", "pL"}));  
        prefijosPorRelacion.add(new Elemento("knows", new String[]{"p", "p"}));
        prefijosPorRelacion.add(new Elemento("postIsLocatedIn", new String[]{"m", "pL"})); 
        
        
        Map<String, String> relationFiles = new HashMap<>();
        relationFiles.put("commentCreator", basePath + File.separator + "dynamic" + File.separator + "comment_hasCreator_person_0_0.csv");
        relationFiles.put("personLikes", basePath + File.separator + "dynamic" + File.separator + "person_likes_comment_0_0.csv");
        relationFiles.put("commentReplyOfComment", basePath + File.separator + "dynamic" + File.separator + "comment_replyOf_comment_0_0.csv");
        relationFiles.put("postCreator", basePath + File.separator + "dynamic" + File.separator + "post_hasCreator_person_0_0.csv");
        relationFiles.put("forumPost", basePath + File.separator + "dynamic" + File.separator + "forum_containerOf_post_0_0.csv");
        relationFiles.put("forumMember", basePath + File.separator + "dynamic" + File.separator + "forum_hasMember_person_0_0.csv");
        relationFiles.put("forumModerator", basePath + File.separator + "dynamic" + File.separator + "forum_hasModerator_person_0_0.csv");
        relationFiles.put("personLikesPost", basePath + File.separator + "dynamic" + File.separator + "person_likes_post_0_0.csv");
        relationFiles.put("personHasInterest", basePath + File.separator + "dynamic" + File.separator + "person_hasInterest_tag_0_0.csv");
        relationFiles.put("forumHasTag", basePath + File.separator + "dynamic" + File.separator + "forum_hasTag_tag_0_0.csv");
        relationFiles.put("postHasTag", basePath + File.separator + "dynamic" + File.separator + "post_hasTag_tag_0_0.csv");
        relationFiles.put("commentHasTag", basePath + File.separator + "dynamic" + File.separator + "comment_hasTag_tag_0_0.csv");
        relationFiles.put("tagIsSubClassOf", basePath + File.separator + "static" + File.separator + "tagclass_isSubclassOf_tagclass_0_0.csv");
        relationFiles.put("commentIsLocatedIn", basePath + File.separator + "dynamic" + File.separator + "comment_isLocatedIn_place_0_0.csv");
        relationFiles.put("personIsLocatedIn", basePath + File.separator + "dynamic" + File.separator + "person_isLocatedIn_place_0_0.csv");
        relationFiles.put("personStudyAt", basePath + File.separator + "dynamic" + File.separator + "person_studyAt_organisation_0_0.csv");
        relationFiles.put("personWorkAt", basePath + File.separator + "dynamic" + File.separator + "person_workAt_organisation_0_0.csv");
        relationFiles.put("placeIsPartOf", basePath + File.separator + "static" + File.separator + "place_isPartOf_place_0_0.csv");
        relationFiles.put("tagHasType", basePath + File.separator + "static" + File.separator + "tag_hasType_tagclass_0_0.csv");
        relationFiles.put("commentReplyOfPost", basePath + File.separator + "dynamic" + File.separator + "comment_replyOf_post_0_0.csv");
        relationFiles.put("organisationIsLocatedIn", basePath + File.separator + "static" + File.separator + "organisation_isLocatedIn_place_0_0.csv");
        relationFiles.put("knows", basePath + File.separator + "dynamic" + File.separator + "person_knows_person_0_0.csv");
        relationFiles.put("postIsLocatedIn", basePath + File.separator + "dynamic" + File.separator + "post_isLocatedIn_place_0_0.csv");

        Map<String, String> titulosEdges = new HashMap<>();
        titulosEdges.put("commentCreator", "hasCreator");
        titulosEdges.put("personLikes", "likes");
        titulosEdges.put("commentReplyOfComment", "replyOf");
        titulosEdges.put("postCreator", "hasCreator");
        titulosEdges.put("forumPost", "containerOf");
        titulosEdges.put("forumMember", "hasMember");
        titulosEdges.put("forumModerator", "hasModerator");
        titulosEdges.put("personLikesPost", "likes");
        titulosEdges.put("personHasInterest", "hasInterest");
        titulosEdges.put("forumHasTag", "hasTag");
        titulosEdges.put("postHasTag", "hasTag");
        titulosEdges.put("commentHasTag", "hasTag");
        titulosEdges.put("tagIsSubClassOf", "isSubclassOf");
        titulosEdges.put("commentIsLocatedIn", "isLocatedIn");
        titulosEdges.put("personIsLocatedIn", "isLocatedIn");
        titulosEdges.put("personStudyAt", "studyAt");
        titulosEdges.put("personWorkAt", "workAt");
        titulosEdges.put("placeIsPartOf", "isPartOf");
        titulosEdges.put("tagHasType", "hasType");
        titulosEdges.put("commentReplyOfPost", "replyOf");
        titulosEdges.put("organisationIsLocatedIn", "isLocatedIn");
        titulosEdges.put("knows", "knows");
        titulosEdges.put("postIsLocatedIn", "isLocatedIn");
        
        

        Map<String, String> idMapping = new HashMap<>();
        //Map<String, String> idMapping2 = new HashMap<>();
        List<String> lineasNodes = new ArrayList<>();
        List<String> lineasEdges = new ArrayList<>();
        AtomicInteger nComment = new AtomicInteger(0);
        AtomicInteger nPost = new AtomicInteger(0);
        System.out.println();
        //int nComment=0;
        //int nPost=0;
        nodeFiles.forEach((key, filePath) -> {
            try {
                File file = new File(filePath);
                Scanner scanner = new Scanner(file);
                int nodeCount = 0;
                List<String> nodeList = new ArrayList<>();
                String prefix = prefijos.getOrDefault(key, "N");
                
                if(key.equals("comment") && nPost.get()>0){
                    nodeCount=nPost.get()+1;
                }
                if(key.equals("post") && nComment.get()>0){
                    nodeCount=nComment.get()+1;
                }
                while (scanner.hasNextLine()) {
                    String[] fila = scanner.nextLine().split("\\|");
                    if (fila.length > 0 && !fila[0].equals("id")) {
                        String originalId = fila[0];
                        String newId = prefix + nodeCount;
                        idMapping.put(prefix + originalId, newId);
                        /*if((prefix+originalId).equals("m618475290625")){
                            System.out.println("jajaj "+prefix + originalId);
                            //System.exit(0);
                        }*/
                        //idMapping2.put(newId, originalId);
                        lineasNodes.add(newId + "," + newId);
                        nodeList.add(newId);
                        nodeCount++;
                        if(key.equals("comment")){
                            nComment.incrementAndGet();
                        }
                        if(key.equals("post")){
                            nPost.incrementAndGet();
                        }
                    
                    }
                }
                System.out.println("NODOS (" + key + "): " + nodeCount);
                //System.out.println("conteo 2");
                //System.out.println(idMapping.size());
                //System.out.println(idMapping2.size());
                scanner.close();

                try (BufferedWriter writer = new BufferedWriter(new FileWriter(resultadosFolder + key + ".csv"))) {
                    for (String nodeId : nodeList) {
                        writer.write(nodeId);
                        writer.newLine();
                    }
                } catch (IOException e) {
                    //System.err.println("Error al escribir el archivo de salida: " + e.getMessage());
                }
            } catch (IOException e) {
                e.printStackTrace();
            }

        });
        //System.out.println(idMapping);
        //System.out.println(nNodos);
        System.out.println("--------------------------------------------------------------------------------");
        System.out.println();
        System.out.println("Numero de nodos:");
        System.out.println(lineasNodes.size());
        System.out.println();
        System.out.println("--------------------------------------------------------------------------------");
        System.out.println();
        // Procesar relaciones

        //AÑADIR VERIFICACION 
        relationFiles.forEach((key, filePath) -> {
            List<String> edgeList = new ArrayList<>();
            try {
                File file = new File(filePath);
                Scanner scanner = new Scanner(file);
                int edgeCount = 0;
                String firstString = null;
                String secondString = null;

                for (Elemento elemento : prefijosPorRelacion) {
                    if (elemento.getStringPrincipal().equals(key)) {
                        String[] secondaryArray = elemento.getArraySecundario();
                        
                        if (secondaryArray.length >= 2) {
                            firstString = secondaryArray[0];  
                            secondString = secondaryArray[1]; 
                        } else {
                        }

                        break;
                    }
                }
             
                while (scanner.hasNextLine()) {
                    String[] fila = scanner.nextLine().split("\\|");
                    if (fila.length > 1 && !fila[0].contains("id")) {
                        String sourceId = idMapping.get(firstString+fila[0]);
                        String targetId = idMapping.get(secondString+fila[1]);
                        //System.out.println(firstString+fila[0]+"  result "+idMapping.get(firstString+fila[0]));
                        //System.out.println(secondString+fila[1]+"  result "+idMapping.get(secondString+fila[1]));
                        if (sourceId != null && targetId != null) {
                            String keyAux=titulosEdges.get(key);
                            String edge = sourceId + "," + keyAux + "," + targetId;
                            edgeList.add(edge);
                            lineasEdges.add(edge);
                            edgeCount++;
                            //nEdges.incrementAndGet();
                        }
                    }
                }
                System.out.println("EDGES (" + key + "): " + edgeCount);
                scanner.close();

                try (BufferedWriter writer = new BufferedWriter(new FileWriter(resultadosFolder + key + ".csv"))) {
                    for (String edge : edgeList) {
                        writer.write(edge);
                        writer.newLine();
                    }
                } catch (IOException e) {
                    //System.err.println("Error al escribir el archivo de salida de relación: " + e.getMessage());
                }   
            } catch (IOException e) {
                e.printStackTrace();
            }

        });

        
        System.out.println("--------------------------------------------------------------------------------");
        System.out.println();
        System.out.println("Numero de aristas:");
        System.out.println(lineasEdges.size());
        System.out.println();
        System.out.println("--------------------------------------------------------------------------------");
        System.out.println();

        try (BufferedWriter nodeWriter = new BufferedWriter(new FileWriter(resultadosMain  + File.separator + "nodes.txt"));
             BufferedWriter edgeWriter = new BufferedWriter(new FileWriter(resultadosMain  + File.separator + "edges.txt"))) {

            for (String nodeLine : lineasNodes) {
                nodeWriter.write(nodeLine);
                nodeWriter.newLine();
            }
            System.out.println("Archivo final de nodos creado: "+resultadosMain + File.separator + "nodes.txt");

            for (String nodeLine : lineasEdges) {
                edgeWriter.write(nodeLine);
                edgeWriter.newLine();
            }
            System.out.println("Archivo final de nodos creado: "+resultadosMain + File.separator + "edges.txt");

        } catch (IOException e) {
            //System.err.println("Error al escribir el archivo final de nodos: " + e.getMessage());
        }
    }
}



class Elemento {
    String stringPrincipal;
    String[] arraySecundario;

    public Elemento(String stringPrincipal, String[] arraySecundario) {
        this.stringPrincipal = stringPrincipal;
        this.arraySecundario = arraySecundario;
    }

    public String getStringPrincipal(){
        return stringPrincipal;
    }

    public String[] getArraySecundario(){
        return arraySecundario;
    }

    @Override
    public String toString() {
        return "Elemento{" +
                "stringPrincipal='" + stringPrincipal + '\'' +
                ", arraySecundario=" + Arrays.toString(arraySecundario) +
                '}';
    }
}