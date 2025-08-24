# PathForge - Path Query Generator for Graph Database Evaluation

A Python tool for systematic generation of path queries (Regular Path Queries) that enables objective and reproducible evaluation of graph database systems.
## Overview

PathForge implements a three-tier hierarchical methodology to generate representative sets of path queries:
- **Abstract Queries**: Abstract patterns using regular expression operators
- **Template Queries**: Concrete instantiations using LDBC-SNB schema relations  
- **Real Queries**: Executable queries anchored to specific graph nodes

## Key Features
✅ **Hierarchical Selection**: Systematic query selection based on the number of path generated  
✅ **Structural Analysis**: Graph connectivity analysis with ranking generation  
✅ **Configurable Workloads**: Customizable query sets for different evaluation objectives  
✅ **Reproducible Methodology**: Eliminates subjective bias in query selection  

## Architecture

The system consists of two complementary tools:

### PathAnalyzer
- **Purpose**: Graph analysis and ranking generation
- **Computational Cost**: High (requires MillenniumDB execution)
- **Output**: Performance-based rankings for abstract/template queries and node connectivity rankings
- **Use Case**: Initial analysis or custom database evaluation

### PathGenerator  
- **Purpose**: Efficient query set generation using pre-computed rankings
- **Computational Cost**: Low
- **Output**: Curated query sets in multiple formats
- **Use Case**: Rapid benchmark generation for standard evaluations

## Abstract Queries Reference

This table shows the complete set of abstract query patterns used by PathForge, along with their standardized notation and query identifiers.

| Abstract Query ID | Pattern |
|-------------------|---------|
| **AQ1** | `a.b` |
| **AQ2** | `a.b.c` |
| **AQ3** | `(a.b)?` |
| **AQ4** | `a.(b\|c)` |
| **AQ5** | `c.(a?)` |
| **AQ6** | `(c?).a` |
| **AQ7** | `a\|b` |
| **AQ8** | `(a.b)\|c` |
| **AQ9** | `(a\|b)\|c` |
| **AQ10** | `a+\|b` |
| **AQ11** | `a*\|b` |
| **AQ12** | `a\|c` |
| **AQ13** | `(a?)\|b` |
| **AQ14** | `c\|(a?)` |
| **AQ15** | `a?` |
| **AQ16** | `a??` |
| **AQ17** | `c\|(a\|b)` |
| **AQ18** | `(a\|b)+` |
| **AQ19** | `(a\|b)?` |
| **AQ20** | `(a\|b)*` |
| **AQ21** | `c\|(a.b)` |
| **AQ22** | `a+.b` |
| **AQ23** | `a*.b` |
| **AQ24** | `a.b+` |
| **AQ25** | `a.b*` |
| **AQ26** | `a\|(a+)` |
| **AQ27** | `a+` |
| **AQ28** | `a*` |

## Prerequisites

### System Requirements
- Linux/Unix environment
- Python 3.7+
- Git
- CMake
- GCC/G++

### Dependencies
```bash
sudo apt update && sudo apt install -y git g++ cmake libssl-dev \
libncurses-dev locales less python3 python3-venv
```

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/dbgutalca/pathforge
cd pathforge
```

### 2. Install MillenniumDB
```bash
sudo locale-gen en_US.UTF-8
git clone https://github.com/MillenniumDB/MillenniumDB.git
cd MillenniumDB
export MDB_HOME=$(pwd)
wget https://archives.boost.io/release/1.82.0/source/boost_1_82_0.tar.gz 
tar -xf boost_1_82_0.tar.gz
mkdir -p $MDB_HOME/third_party/boost_1_82/include
mv boost_1_82_0/boost $MDB_HOME/third_party/boost_1_82/include
rm -r boost_1_82_0.tar.gz boost_1_82_0
cmake -Bbuild/Release -DCMAKE_BUILD_TYPE=Release
cmake --build build/Release/ -j $(nproc)
```

### 3. Prepare LDBC-SNB Database

#### Option A: Download Pre-compiled Dataset
Download from

#### Option B: Generate Using DATAGEN
Follow [LDBC-SNB DATAGEN instructions](https://github.com/ldbc/ldbc_snb_datagen_spark) to generate custom scale factors.

### 4. Process Database Files
```bash
# Process CSV files (outside the CSV folder)
# You should replace [LDBC_DB] with the folder of the LDBC
java csvParser.java [LDBC_DB]

# Create Quad Model
python3 createQuadModel.py

# Import to MillenniumDB
cd MillenniumDB
build/Release/bin/mdb-import NEW_DB.QM /data/db/SCALE_FACTOR
```

## Usage

### Quick Start (Recommended)
For rapid query set generation using pre-computed rankings:

```bash
python3 pathGenerator.py --use-rankings 01 --aq 2 --tq 3 --rq 5
```

### Advanced Usage

#### PathAnalyzer - Complete Analysis
Generate custom rankings with full configurability:

```bash
python3 pathAnalyzer.py --nodes-per-label 3 \
--node-selection-mode max+med --db-path ./data/db/03
```

**Parameters:**
- `--nodes-per-label`: Number of nodes to select per relation label (default: 3)
- `--node-selection-mode`: Node selection criteria (`max`, `min`, `med`, `.25`, `.75`, or combinations like `max+min`)
- `--db-path`: Path to MillenniumDB database (defaults to `01` if omitted)

#### PathGenerator - Efficient Generation
Create query sets using existing or newly generated rankings:

```bash
python3 pathGenerator.py --aq 2 --tq 3 --rq 5 --node-selection-mode max
```

**Parameters:**
- `--use-rankings SCALE`: Use pre-computed rankings from specific scale factor (`01`, `03`, `1`, `3`)
- `--aq N`: Number of abstract queries to select (top N from ranking)
- `--tq M`: Number of template queries per abstract query  
- `--rq P`: Number of real queries per template query
- `--node-selection-mode`: Node selection mode for real queries (`max`, `min`, `med`)
- `--file-expressions FILE`: XLSX file containing query language expressions for automatic query transformation (optional). The file must contain columns: Abstract_Query and Translation to map each abstract query to its equivalent expression in the target query language

PathGenerator with Query Language Transformation
Generate queries with automatic transformation to target query language:
```bash
python3 pathGenerator.py --use-rankings 03 --aq 5 --tq 2 --rq 3 \
--node-selection-mode max --file-expressions language-expressions.xlsx
```
Note: An example file gql.xlsx is provided to demonstrate the required format and structure.

## Configuration Examples

### Minimal Test Set
```bash
python3 pathGenerator.py --use-rankings 01 --aq 1 --tq 2 --rq 1
# Output: 2 queries (1×2×1)
```

### Custom Analysis + Generation
```bash
# Step 1: Generate custom rankings
python3 pathAnalyzer.py --nodes-per-label 5 --node-selection-mode max+min+med

# Step 2: Use generated rankings
python3 pathGenerator.py --aq 3 --tq 3 --rq 2
# Output: 18 queries (3×3×2)
```

## Output Files

### PathAnalyzer Outputs
- `resultados_analyzer01/`: Directory containing analysis results
  - `abstract_queries_rank.xlsx`: Abstract query performance rankings
  - `all_queries.xlsx`: Complete query execution results
  - `paths_and_times_per_real_query.xlsx`: Detailed metrics per real query
  - `template_queries_rank.xlsx`: Template query rankings by abstract query
- `rankingsNodes/`: Directory containing node connectivity rankings per relation

### PathGenerator Outputs  
- `resultados_generator_/`: Directory containing generation results
  - `queries_full.xlsx`: Complete curated query set with metrics
  - `queries_short.csv`: Summary query information in CSV format
  - `queries.txt`: Executable queries in text format

## File Structure
```
pathforge/
├── pathAnalyzer.py          # analysis tool
├── pathGenerator.py         # Efficient query generation tool
├── abstractQueries.txt      # Abstract query patterns
├── templateQueries.txt      # Template query definitions
├── csvParser.java          # CSV processing utility
├── createQuadModel.py      # Quad model generation
├── MillenniumDB/           # Database system directory
├── resultados_analyzer01/  # PathAnalyzer output directory
│   ├── abstract_queries_rank.xlsx
│   ├── all_queries.xlsx
│   ├── paths_and_times_per_real_query.xlsx
│   └── template_queries_rank.xlsx
├── resultados_generator_/  # PathGenerator output directory
│   ├── queries_full.xlsx
│   ├── queries_short.csv
│   └── queries.txt
```

---

**PathForge** - A Python tool for systematic generation of path queries (Regular Path Queries) that enables objective and reproducible evaluation of graph database systems
