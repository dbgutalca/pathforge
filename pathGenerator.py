#!/usr/bin/env python3
import os
import sys
import time
import pandas as pd
import argparse
import re
import csv

class PathBenchAnalizer:
    
    def __init__(self, selective_queries=None, use_rankings="", node_selection_mode="max", cypher_expressions_path=None):
        self.rankings_scale = use_rankings
        self.cypher_expressions_path = cypher_expressions_path
        
        if selective_queries is None:
            selective_queries = {
                'n_abstract': '*',
                'n_templates': '*', 
                'n_real': 3
            }
        
        self.selective_queries = selective_queries
        self.nodes_per_label = self.selective_queries.get('n_real', 3)
        
        self.selection_mode = node_selection_mode.lower() if isinstance(node_selection_mode, str) else "max"
        
        

    def show_welcome_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Colores más vibrantes
        CYAN = '\033[96m'
        MAGENTA = '\033[95m'
        YELLOW = '\033[93m'
        GREEN = '\033[92m'
        BLUE = '\033[94m'
        RED = '\033[91m'
        WHITE = '\033[97m'
        BOLD = '\033[1m'
        RESET = '\033[0m'
        
        print(f"{CYAN}{'═' * 80}{RESET}")
        print(f"{CYAN}║{RESET}" + " " * 78 + f"{CYAN}║{RESET}")
        

        logo_lines = [
            " ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ ",
            "██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗",
            "██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝",
            "██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗",
            "╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║",
            " ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝"
        ]
        
        for i, line in enumerate(logo_lines):
            padding = (78 - len(line)) // 2
            if i < 3:
                colored_line = f"{BOLD}{MAGENTA}{line}{RESET}"
            else:
                colored_line = f"{BOLD}{BLUE}{line}{RESET}"
            print(f"{CYAN}║{RESET}{' ' * padding}{colored_line}{' ' * (78 - padding - len(line))}{CYAN}║{RESET}")
        
        print(f"{CYAN}║{RESET}" + " " * 78 + f"{CYAN}║{RESET}")
        print(f"{CYAN}{'═' * 80}{RESET}")
        
        subtitle = "◆ QUERY GENERATOR◆"
        padding = (80 - len(subtitle)) // 2
        print(f"{' ' * padding}{BOLD}{YELLOW}{subtitle}{RESET}")
        
        print(f"\n{MAGENTA}◇─────◇{RESET}" + f"{BLUE}{'─' * 20}{RESET}" + f"{GREEN}◆{RESET}" + f"{BLUE}{'─' * 20}{RESET}" + f"{MAGENTA}◇─────◇{RESET}")
        time.sleep(2)
        print(f"\n{WHITE}╔{'═' * 50}╗{RESET}")
        print(f"{WHITE}║{RESET} {GREEN}▶{RESET} {BOLD}Developer:{RESET}     J. Núñez                    {WHITE}{RESET}")
        print(f"{WHITE}║{RESET} {GREEN}▶{RESET} {BOLD}Organization:{RESET}  Utalca                      {WHITE}{RESET}")
        print(f"{WHITE}║{RESET} {GREEN}▶{RESET} {BOLD}Version:{RESET}       1.0    {WHITE}{RESET}")
        print(f"{WHITE}╚{'═' * 50}╝{RESET}")
        time.sleep(1)
        if hasattr(self, 'selective_queries') and self.selective_queries:
            aq = self.selective_queries.get('n_abstract', '*')
            tq = self.selective_queries.get('n_templates', '*')
            rq = self.selective_queries.get('n_real', 3)
            print(f"\n{CYAN}┌─── Configuration ─────────────────────────────┐{RESET}")
            scale_display = "01" if not self.rankings_scale else f"{self.rankings_scale:>3}"
            print(f"{CYAN}{RESET} {BOLD}Scale Factor:{RESET}    {YELLOW}{scale_display}{RESET}                    {CYAN}{RESET}")
            print(f"{CYAN}{RESET} {BOLD}Abstract Queries:{RESET}  {YELLOW}{str(aq):>3}{RESET} ", end="")
            print(f"{'[ALL]' if aq == '*' else '':<15} {CYAN}{RESET}")
            print(f"{CYAN}{RESET} {BOLD}Templates/Query:{RESET}   {YELLOW}{str(tq):>3}{RESET} ", end="")
            print(f"{'[ALL]' if tq == '*' else '':<15} {CYAN}{RESET}")
            print(f"{CYAN}{RESET} {BOLD}Real Queries:{RESET}  {YELLOW}{str(rq):>3}{RESET} ", end="")
            print(f"{'':<15} {CYAN}{RESET}")
            print(f"{CYAN}{RESET} {BOLD}Node Selection:{RESET}    {YELLOW}{self.selection_mode:<15}{RESET} {CYAN}{RESET}")
            if self.cypher_expressions_path:
                cypher_name = os.path.basename(self.cypher_expressions_path)
                print(f"{CYAN}{RESET} {BOLD}Language File:{RESET}       {YELLOW}{cypher_name:<15}{RESET} {CYAN}{RESET}")
            print(f"{CYAN}└───────────────────────────────────────────────┘{RESET}")
        
        
        print(f"\n{MAGENTA}{'╍' * 80}{RESET}\n")
        time.sleep(1)

    def validate_cypher_expressions_file(self):
        if not self.cypher_expressions_path:
            return True  
        
        if not os.path.exists(self.cypher_expressions_path):
            print(f"❌ Error: Archivo de expresiones  no encontrado: {self.cypher_expressions_path}")
            return False
        
        try:
            df = pd.read_excel(self.cypher_expressions_path)
            required_columns = ['Abstract_Query', 'Translation']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                print(f"❌ Error: Columnas faltantes en {self.cypher_expressions_path}: {missing_columns}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error validando archivo Cypher: {e}")
            return False

    def validate_rankings_exist(self):
        if self.rankings_scale:
            ranking_base_path = os.path.join("rankings", self.rankings_scale)
        else:
            ranking_base_path = "rankings"
        ranking_base_path = os.path.join("rankings", self.rankings_scale)
        
        print(f"\n🔍 Validando rankings en: {ranking_base_path}")
        
        if not os.path.exists(ranking_base_path):
            print(f"❌ Carpeta no encontrada: {ranking_base_path}")
            return False
        
        required_files = [
            "abstract_queries_rank.xlsx",
            "template_queries_rank.xlsx"
        ]
        
        missing_files = []
        for file in required_files:
            file_path = os.path.join(ranking_base_path, file)
            if not os.path.exists(file_path):
                missing_files.append(file)
            else:
                print(f"✅ Encontrado: {file}")
        
        rankings_nodes_path = os.path.join(ranking_base_path, "rankingsNodes")
        if not os.path.exists(rankings_nodes_path):
            print(f"⚠️  Carpeta rankingsNodes no encontrada: {rankings_nodes_path}")
            print("   (Se generarán mapeos básicos si son necesarios)")
        else:
            print(f"✅ Encontrado: rankingsNodes/")
            try:
                node_files = [f for f in os.listdir(rankings_nodes_path) if f.endswith('.txt')]
                print(f"   📄 {len(node_files)} archivos de nodos disponibles")
            except Exception as e:
                print(f"   ⚠️  Error leyendo rankingsNodes: {e}")
        
        if missing_files:
            print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
            return False
        
        print(f"✅ Rankings válidos encontrados en: rankings/{self.rankings_scale}/")
        return True

    def load_node_mappings_from_rankings_with_selection(self):
        """Carga mapeos usando UN SOLO modo de selección"""
        rankings_nodes_path = os.path.join("rankings", self.rankings_scale, "rankingsNodes")
        
        if not os.path.exists(rankings_nodes_path):
            print("⚠️  No se encontró rankingsNodes/. Usando mapeos por defecto.")
            return self.get_default_node_mappings()
        
        mappings = {}
        try:
            for filename in os.listdir(rankings_nodes_path):
                if filename.endswith('.txt'):
                    label = filename[:-4]
                    file_path = os.path.join(rankings_nodes_path, filename)
                    
                    # Leer TODOS los nodos del archivo ranking
                    all_nodes = []
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                parts = line.split(',')
                                if len(parts) >= 3:  # Posición, NodeID, Conexiones
                                    try:
                                        position = int(parts[0])
                                        node_id = parts[1].strip()
                                        connections = int(parts[2])
                                        all_nodes.append((node_id, connections))
                                    except ValueError:
                                        continue
                    
                    if all_nodes:
                        # Aplicar UN SOLO modo de selección
                        selected_nodes = self.select_nodes_by_single_mode(all_nodes, label)
                        mappings[label] = selected_nodes
            
            return mappings
            
        except Exception as e:
            print(f"❌ Error cargando mapeos desde rankings: {e}")
            return self.get_default_node_mappings()

    def select_nodes_by_single_mode(self, all_nodes, label):
        """Selecciona nodos usando UN SOLO modo"""
        if not all_nodes:
            return []
        
        sorted_nodes = sorted(all_nodes, key=lambda x: x[1], reverse=True)
        total_nodes = len(sorted_nodes)
        
        selected_nodes = []
        
        if self.selection_mode == "max":
            num_nodes = min(self.nodes_per_label, len(sorted_nodes))
            selected_nodes = [node[0] for node in sorted_nodes[:num_nodes]]
        
        elif self.selection_mode == "min":
            valid_nodes = [node for node in sorted_nodes if node[1] > 0]
            if valid_nodes:
                valid_nodes.sort(key=lambda x: x[1])  # Ascendente para min
                num_nodes = min(self.nodes_per_label, len(valid_nodes))
                selected_nodes = [node[0] for node in valid_nodes[:num_nodes]]
        
        elif self.selection_mode == "med":
            if len(sorted_nodes) <= self.nodes_per_label:
                selected_nodes = [node[0] for node in sorted_nodes]
            else:
                median_idx = len(sorted_nodes) // 2
                half_count = self.nodes_per_label // 2
                remainder = self.nodes_per_label % 2
                
                start_idx = max(0, median_idx - half_count)
                end_idx = min(len(sorted_nodes), median_idx + half_count + remainder)
                
                if start_idx == 0:
                    end_idx = min(len(sorted_nodes), self.nodes_per_label)
                elif end_idx == len(sorted_nodes):
                    start_idx = max(0, len(sorted_nodes) - self.nodes_per_label)
                
                selected_nodes = [node[0] for node in sorted_nodes[start_idx:end_idx]]
        
        elif self.selection_mode == ".25":
            if len(sorted_nodes) <= self.nodes_per_label:
                selected_nodes = [node[0] for node in sorted_nodes]
            else:
                p25_idx = len(sorted_nodes) // 4
                half_count = self.nodes_per_label // 2
                remainder = self.nodes_per_label % 2
                
                start_idx = max(0, p25_idx - half_count)
                end_idx = min(len(sorted_nodes), p25_idx + half_count + remainder)
                
                if start_idx == 0:
                    end_idx = min(len(sorted_nodes), self.nodes_per_label)
                elif end_idx == len(sorted_nodes):
                    start_idx = max(0, len(sorted_nodes) - self.nodes_per_label)
                
                selected_nodes = [node[0] for node in sorted_nodes[start_idx:end_idx]]
        
        elif self.selection_mode == ".75":
            if len(sorted_nodes) <= self.nodes_per_label:
                selected_nodes = [node[0] for node in sorted_nodes]
            else:
                p75_idx = (len(sorted_nodes) * 3) // 4
                half_count = self.nodes_per_label // 2
                remainder = self.nodes_per_label % 2
                
                start_idx = max(0, p75_idx - half_count)
                end_idx = min(len(sorted_nodes), p75_idx + half_count + remainder)
                
                if start_idx == 0:
                    end_idx = min(len(sorted_nodes), self.nodes_per_label)
                elif end_idx == len(sorted_nodes):
                    start_idx = max(0, len(sorted_nodes) - self.nodes_per_label)
                
                selected_nodes = [node[0] for node in sorted_nodes[start_idx:end_idx]]
        
        return selected_nodes

    def get_default_node_mappings(self):
        return {
            "hasCreator": ["m135702"],
            "containerOf": ["f38"],
            "hasMember": ["f41"],
            "knows": ["p4"]
        }

    def read_ranking_abstract_from_rankings(self):
        if self.rankings_scale:
            ranking_path = os.path.join("rankings", self.rankings_scale, "abstract_queries_rank.xlsx")
        else:
            ranking_path = os.path.join("rankings", "abstract_queries_rank.xlsx")
            
        if not os.path.exists(ranking_path):
            print(f"❌ Error: No se encontró {ranking_path}")
            return []
        
        try:
            df = pd.read_excel(ranking_path, sheet_name='Ranking')
            return df.to_dict('records')
        except Exception as e:
            print(f"❌ Error leyendo {ranking_path}: {e}")
            return []

    def read_ranking_templates_from_rankings(self, q_number):
        if self.rankings_scale:
            ranking_path = os.path.join("rankings", self.rankings_scale, "template_queries_rank.xlsx")
        else:
            ranking_path = os.path.join("rankings", "template_queries_rank.xlsx")
        
        if not os.path.exists(ranking_path):
            print(f"❌ Error: No se encontró {ranking_path}")
            return []
        
        sheet_name = f"Q{q_number}"
        try:
            df = pd.read_excel(ranking_path, sheet_name=sheet_name)
            return df.to_dict('records')
        except Exception as e:
            print(f"❌ Error leyendo sheet {sheet_name} de {ranking_path}: {e}")
            return []

    def extract_initial_label(self, pattern):
        """Extrae la etiqueta inicial de un patrón de consulta"""
        import re
        
        # Buscar patrones como (:etiqueta
        match = re.search(r':([a-zA-Z0-9_]+)', pattern)
        if match:
            return match.group(1)
        return None

    def generate_real_queries_from_template(self, template, n_real):
        if not isinstance(template, str):
            print(f"Template no es string: {type(template)} - {template}")
            return []
        
        initial_label = self.extract_initial_label(template)
        if not initial_label:
            print(f"No se pudo extraer etiqueta de template: {template}")
            return []
        
        if not hasattr(self, 'node_mappings') or not self.node_mappings:
            self.node_mappings = self.load_node_mappings_from_rankings_with_selection()
        
        if initial_label not in self.node_mappings:
            print(f"No se encontró mapeo para etiqueta: {initial_label}")
            return []
        
        node_ids = self.node_mappings[initial_label][:n_real]
        real_queries = []
        
        for node_id in node_ids:
            query = template.replace("(x)=", f"({node_id})=")
            real_queries.append(query)
        
        return real_queries

    def generate_pool_from_rankings(self):
        
        n_abstract = self.selective_queries.get('n_abstract', '*')
        n_templates = self.selective_queries.get('n_templates', '*')
        n_real = self.selective_queries.get('n_real', 3)
        
        abstract_ranking = self.read_ranking_abstract_from_rankings()
        if not abstract_ranking:
            print("❌ Error: No se pudo cargar ranking abstracto")
            return
        
        if n_abstract == '*':
            selected_abstracts = abstract_ranking
        else:
            selected_abstracts = abstract_ranking[:n_abstract]
        
        self.node_mappings = self.load_node_mappings_from_rankings_with_selection()
        
        pool_queries = []
        
        for i, abstract_item in enumerate(selected_abstracts):
            q_number_str = abstract_item.get('AQ Code', '').replace('Q', '')
            if not q_number_str:
                continue
                
            try:
                q_number = int(q_number_str)
            except:
                continue
            
            template_ranking = self.read_ranking_templates_from_rankings(q_number)
            if not template_ranking:
                print(f"   ⚠️  No se encontraron templates para Q{q_number}")
                continue
            
            if n_templates == '*':
                selected_templates = template_ranking
            else:
                selected_templates = template_ranking[:n_templates]
            
            for template_item in selected_templates:
                template_query = template_item.get('Template Query', '')
                if not isinstance(template_query, str) or not template_query.strip():
                    continue
                
                real_queries = self.generate_real_queries_from_template(template_query, n_real)
                
                for real_query in real_queries:
                    promedio_paths = template_item.get('Promedio Paths', 0)
                    if isinstance(promedio_paths, (int, float)):
                        promedio_paths = int(round(promedio_paths))
                    
                    pool_queries.append({
                        'Q_Number': f"Q{q_number}",
                        'Abstract_Pattern': abstract_item.get('AQ', ''),
                        'Template_Query': template_query,
                        'Real_Query': real_query,
                        'Initial_Label': self.extract_initial_label(template_query),
                    })
        
        print(f"\n✅ Consultas generadas: {len(pool_queries)} consultas")
        
        self.save_pool_from_rankings(pool_queries)

    def save_pool_from_rankings(self, pool_queries):
        if not pool_queries:
            print("❌ No hay consultas en el pool para guardar")
            return
        
        output_folder = f"resultados_generator_{self.rankings_scale}"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        df = pd.DataFrame(pool_queries)
        
        csv_path = self.generate_structured_csv_corrected(pool_queries, output_folder)
        
        self.save_standard_queries_txt(pool_queries, output_folder)
        
        if self.cypher_expressions_path:
            self.apply_cypher_transformation(csv_path, output_folder)


    def save_standard_queries_txt(self, pool_queries, output_folder):
            """
            Guarda todas las queries reales en formato estándar en un archivo .txt
            Una query por línea, sin metadatos adicionales
            """
            try:
                txt_output_path = os.path.join(output_folder, "queries.txt")
                
                real_queries = [query_data.get('Real_Query', '') for query_data in pool_queries if query_data.get('Real_Query', '').strip()]
                
                with open(txt_output_path, 'w', encoding='utf-8') as f:
                    for query in real_queries:
                        f.write(f"{query}\n")
                
                print(f"📄 TXT estándar: {txt_output_path}")
                print(f"   📊 {len(real_queries)} queries en formato estándar guardadas")
                
                return txt_output_path
                
            except Exception as e:
                print(f"❌ Error guardando TXT estándar: {e}")
                return None

    def extract_query_structure(self, real_query):
        """
        Extrae la estructura de una consulta real para el CSV
        Retorna: (source_node, [relaciones])
        """
        source_pattern = r'\(([^)]+)\)=\['
        source_match = re.search(source_pattern, real_query)
        source_node = source_match.group(1) if source_match else ""
        
        relations_pattern = r':([a-zA-Z0-9_]+)(?:\{[^}]*\})?'
        relations_matches = re.findall(relations_pattern, real_query)
        
        relations = []
        seen = set()
        for rel in relations_matches:
            if rel not in seen:
                relations.append(rel)
                seen.add(rel)
        
        return source_node, relations

    def load_mapping_queries_csv(self):
        """
        Carga el archivo mappingQueries.csv para obtener los mapeos correctos AQ-TQ-Query
        """
        mapping_file = "mappingQueries.csv"
        if not os.path.exists(mapping_file):
            return {}
        
        mapping_dict = {}
        try:
            with open(mapping_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    aq = row.get('AQ', '').strip()
                    tq = row.get('TQ', '').strip()
                    query = row.get('Query', '').strip()
                    
                    if aq and tq and query:
                        mapping_dict[query] = {
                            'AQ': aq,
                            'TQ': tq
                        }
            
            print(f"✅ Cargados {len(mapping_dict)} mapeos desde {mapping_file}")
            return mapping_dict
            
        except Exception as e:
            print(f"❌ Error cargando {mapping_file}: {e}")
            return {}

    def find_matching_aq_tq(self, template_query, real_query):
        """
        Encuentra los valores correctos de AQ y TQ comparando con mappingQueries.csv
        """
        if not hasattr(self, 'mapping_csv_dict'):
            self.mapping_csv_dict = self.load_mapping_queries_csv()
        
        mapping_dict = self.mapping_csv_dict
        
        if template_query in mapping_dict:
            return mapping_dict[template_query]['AQ'], mapping_dict[template_query]['TQ']
        
        template_pattern = re.sub(r'\([^)]+\)=', '(x)=', real_query)
        
        for mapped_query, mapping_data in mapping_dict.items():
            mapped_pattern = re.sub(r'\([^)]+\)=', '(x)=', mapped_query)
            if template_pattern == mapped_pattern:
                return mapping_data['AQ'], mapping_data['TQ']
        
        real_relations = set(re.findall(r':([a-zA-Z0-9_]+)', real_query))
        
        for mapped_query, mapping_data in mapping_dict.items():
            mapped_relations = set(re.findall(r':([a-zA-Z0-9_]+)', mapped_query))
            if real_relations == mapped_relations:
                return mapping_data['AQ'], mapping_data['TQ']
        
        return None, None

    def generate_structured_csv_corrected(self, pool_queries, output_folder):
        """
        Nueva versión de generate_structured_csv que usa mappingQueries.csv
        Con TQ corregidos que siguen patrón lógico por AQ
        """
        csv_path = os.path.join(output_folder, "queries_short.csv")
        
        aq_template_counters = {}
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            writer.writerow(['AQ', 'TQ', 'source_node', '%1', '%2', '%3', '%4'])
            
            for query_data in pool_queries:
                real_query = query_data.get('Real_Query', '')
                template_query = query_data.get('Template_Query', '')
                q_number_fallback = query_data.get('Q_Number', '')
                
                aq_value, tq_value = self.find_matching_aq_tq(template_query, real_query)
                
                if aq_value is None or tq_value is None:
                    aq_value = q_number_fallback  # Q25, Q24, etc.
                    
                    if aq_value not in aq_template_counters:
                        aq_template_counters[aq_value] = {}
                    
                    template_key = abs(hash(template_query)) % 10000
                    
                    if template_key not in aq_template_counters[aq_value]:
                        counter = len(aq_template_counters[aq_value]) + 1
                        aq_template_counters[aq_value][template_key] = counter
                    
                    template_num = aq_template_counters[aq_value][template_key]
                    tq_value = f"{aq_value.replace('Q', 'T')}.{template_num:02d}"
                
                source_node, relations = self.extract_query_structure(real_query)
                
                row = [aq_value, tq_value, source_node]
                
                for i in range(4):
                    if i < len(relations):
                        row.append(relations[i])
                    else:
                        row.append("")
                
                writer.writerow(row)
        
        return csv_path

    
    def load_cypher_expressions(self):
        """Carga el archivo de expresiones Cypher"""
        try:
            cypher_df = pd.read_excel(self.cypher_expressions_path)
            return cypher_df
        except Exception as e:
            print(f"❌ Error cargando expresiones Cypher: {e}")
            return None

    def transform_single_query(self, query_row, cypher_expressions):
        """Transforma una fila de query usando las expresiones de Cypher"""
        try:
            aq = query_row['AQ']
            
            cypher_row = cypher_expressions[cypher_expressions['Abstract_Query'] == aq]
            
            if cypher_row.empty:
                print(f"⚠️  No se encontró expresión Cypher para AQ = {aq}")
                return None
            
            cypher_expression = cypher_row['Translation'].iloc[0]
            
            if 'source_node' in query_row and pd.notna(query_row['source_node']):
                cypher_expression = cypher_expression.replace('source_node', str(query_row['source_node']))
            
            for i in range(1, 5):
                placeholder = f'%{i}'
                column_name = f'%{i}'
                
                if column_name in query_row and pd.notna(query_row[column_name]):
                    cypher_expression = cypher_expression.replace(placeholder, str(query_row[column_name]))
            
            return cypher_expression
            
        except Exception as e:
            print(f"❌ Error transformando query {query_row.get('AQ', 'unknown')}: {e}")
            return None


    def apply_cypher_transformation(self, csv_path, output_folder):
            """Aplica la transformación Cypher al CSV generado"""
            try:
                
                cypher_df = self.load_cypher_expressions()
                if cypher_df is None:
                    return False
                
                queries_df = pd.read_csv(csv_path)
                
                required_columns = ['AQ', 'TQ', 'source_node']
                missing_columns = [col for col in required_columns if col not in queries_df.columns]
                if missing_columns:
                    return False
                
                results = []
                successful_transforms = 0
                failed_transforms = 0
                
                print(f"🔄 Transformando {len(queries_df)} queries...")
                
                for index, row in queries_df.iterrows():
                    RQ = self.transform_single_query(row, cypher_df)
                    
                    # Crear una nueva fila con todos los datos originales más la query transformada
                    result_row = row.to_dict()
                    result_row['RQ'] = RQ
                    results.append(result_row)
                    
                    if RQ:
                        successful_transforms += 1
                    else:
                        failed_transforms += 1
                
                results_df = pd.DataFrame(results)
                excel_output_path = os.path.join(output_folder, "queries_full.xlsx")
                results_df.to_excel(excel_output_path, index=False)
                
                txt_output_path = self.save_transformed_queries_txt(results_df, output_folder)
                
                # Mostrar estadísticas finales
                print(f"\n✅ Transformación completada!")
                print(f"📁 Archivos generados:")
                print(f"   📊 Excel: {excel_output_path}")
                if txt_output_path:
                    print(f"   📄 TXT: {txt_output_path}")
                print(f"📈 Total de queries procesadas: {len(results_df)}")
                print(f"✅ Transformaciones exitosas: {successful_transforms}")
                if failed_transforms > 0:
                    print(f"❌ Transformaciones fallidas: {failed_transforms}")
                
                return True
                
            except Exception as e:
                print(f"❌ Error en la transformación Cypher: {e}")
                return False


    def save_transformed_queries_txt(self, results_df, output_folder):
            """
            Guarda solo las queries transformadas en un archivo .txt
            Una query por línea, sin metadatos adicionales
            """
            try:
                txt_output_path = os.path.join(output_folder, "queries.txt")
                
                # Filtrar solo las queries que se transformaron exitosamente
                successful_queries = results_df[results_df['RQ'].notna()]['RQ']
                
                # Guardar una query por línea
                with open(txt_output_path, 'w', encoding='utf-8') as f:
                    for query in successful_queries:
                        f.write(f"{query}\n")
                
                #print(f"📄 TXT transformado: {txt_output_path}")
                #print(f"   📊 {len(successful_queries)} queries transformadas guardadas")
                
                return txt_output_path
                
            except Exception as e:
                print(f"❌ Error guardando TXT transformado: {e}")
                return None

    def run(self):
        """Método principal para ejecutar el proceso"""
        self.show_welcome_screen()

        
        # Validar rankings
        if not self.validate_rankings_exist():
            print(f"❌ ERROR: No se encontraron rankings válidos en rankings/{self.rankings_scale}/")
            print("💡 Debe tener los archivos abstract_queries_rank.xlsx y template_queries_rank.xlsx")
            input("\nPresione Enter para salir...")
            return
        
        # Validar archivo Cypher si se proporcionó
        if self.cypher_expressions_path and not self.validate_cypher_expressions_file():
            print("❌ ERROR: Archivo de expresiones inválido")
            input("\nPresione Enter para salir...")
            return
        
        # Generar pool (esto incluirá la transformación automáticamente)
        self.generate_pool_from_rankings()
        
        print("\n🎉 ¡Proceso completado exitosamente!")
        if self.cypher_expressions_path:
            print("   📊 Consultas generadas desde rankings")
            print(f"   📁 Archivos disponibles en: resultados_generator_{self.rankings_scale}/")
        
        input("\nPresione Enter para salir...")

def validate_select_query(value):
    if value == '*':
        return '*'
    try:
        int_value = int(value)
        if int_value > 0:
            return int_value
        else:
            raise argparse.ArgumentTypeError("El número debe ser mayor que 0")
    except ValueError:
        raise argparse.ArgumentTypeError("Debe ser un número entero positivo o '*'")


def validate_selection_mode(value):
    valid_modes = ["max", "med", "min", ".25", ".75"]
    if value.lower() in valid_modes:
        return value.lower()
    else:
        raise argparse.ArgumentTypeError(
            f"Modo inválido: {value}. Los modos válidos son: max, med, min, .25, .75"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generador de pool de consultas desde rankings con transformación Cypher integrada',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  
  # Generación básica sin transformación Cypher
  python pathGenerator.py --use-rankings 03
  
  # Generación CON transformación Cypher automática
  python pathGenerator.py --use-rankings 03 --file-expressions cypher-expressions.xlsx
  
  # Combinando con otros parámetros
  python pathGenerator.py --use-rankings 1 --aq 5 --tq 2 --rq 6 --node-selection-mode max --file-expressions cypher-expressions.xlsx
  
  # Diferentes modos de selección de nodos
  python pathGenerator.py --use-rankings 03 --node-selection-mode min --file-expressions cypher-expressions.xlsx
  python pathGenerator.py --use-rankings 03 --node-selection-mode med --file-expressions cypher-expressions.xlsx
  
        """
    )
    
    parser.add_argument('--use-rankings', type=str, default='',
                        help='Scale factor de los rankings a usar (default: rankings)')
    parser.add_argument('--aq', type=validate_select_query, default='*',
                        help='Abstract queries a seleccionar: número o "*" (default: *)')
    parser.add_argument('--tq', type=validate_select_query, default='*',
                        help='Templates por abstract query: número o "*" (default: *)')
    parser.add_argument('--rq', type=int, default=3,
                        help='Consultas reales por template (default: 3)')
    parser.add_argument('--node-selection-mode', type=validate_selection_mode, default='max',
                        help='Modo de selección de nodos: max, med, min, .25, .75 (default: max)')
    parser.add_argument('--file-expressions', type=str, default=None,
                        help='Archivo Excel con expresiones Cypher para transformación automática (opcional)')
    
    args = parser.parse_args()
    
    # Validar archivo Cypher si se proporcionó - CORREGIDO
    if args.file_expressions and not os.path.exists(args.file_expressions):
        print(f"❌ Error: Archivo de expresiones no encontrado: {args.file_expressions}")
        sys.exit(1)
    
    selective_queries = {
        'n_abstract': args.aq,
        'n_templates': args.tq,
        'n_real': args.rq
    }
    
    benchmark = PathBenchAnalizer(
        selective_queries=selective_queries,
        use_rankings=args.use_rankings,
        node_selection_mode=args.node_selection_mode,
        cypher_expressions_path=args.file_expressions  # CORREGIDO
    )
    
    benchmark.run()