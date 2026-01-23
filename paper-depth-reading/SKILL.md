---
name: paper-depth-reading
description: Comprehensive academic paper analysis skill for computer graphics and AI research papers. Use when Claude needs to perform deep, structured analysis of academic papers with code implementation.
---

# Paper Depth Reading Skill

## Overview

This skill provides a structured framework for deep analysis of academic papers, particularly in computer graphics, computer vision, and AI research. It guides Claude through a comprehensive reading process that connects theoretical concepts with practical code implementations.

## Core Workflow

### 1. Initial Paper Assessment (10 minutes)
- **Read abstract, introduction, and conclusion** to understand core contributions
- **Identify key sections**: methodology, experiments, results
- **Skim figures and tables** to grasp visual results
- **Note paper structure** and main contributions

### 2. Code Repository Exploration
Before deep reading, always explore the code repository:
- **Examine directory structure** to understand project organization
- **Identify key modules**: models, training scripts, datasets, utils
- **Read configuration files** to understand hyperparameters
- **Check README** for setup instructions and dependencies

### 3. Detailed Methodology Analysis
- **Network architecture**: Layer-by-layer analysis with shape transformations
- **Loss functions**: Mathematical formulation and implementation
- **Training pipeline**: Data flow and optimization details
- **Dataset processing**: Preprocessing and augmentation strategies

### 4. Code-Paper Connection
- **Cross-reference**: Connect paper descriptions to actual code implementations
- **Clarify ambiguities**: Use code to resolve unclear paper descriptions
- **Verify details**: Check implementation specifics against paper claims
- **Identify extensions**: Note code features not mentioned in paper

### 5. Critical Analysis
- **Strengths**: What makes this approach effective?
- **Limitations**: What are the constraints or weaknesses?
- **Comparisons**: How does it compare to related work?
- **Future directions**: What improvements are possible?

## Analysis Framework

### Input Analysis
- **Data type**: Images, point clouds, text, video, etc.
- **Shape specification**: Exact dimensions (e.g., `[B, C, H, W]`, `[B, N, D]`)
- **Preprocessing**: Normalization, augmentation, encoding
- **Special considerations**: Multi-modal inputs, temporal sequences

### Output Analysis  
- **Target format**: Generated images, 3D models, predictions, etc.
- **Shape specification**: Output dimensions and format
- **Post-processing**: Decoding, rendering, evaluation metrics

### Methodology Breakdown
For each component:
1. **Component name** and purpose
2. **Mathematical formulation** (LaTeX format)
3. **Implementation details** from code
4. **Shape transformations** through the pipeline
5. **Hyperparameters** and configuration

### Experimental Results
- **Quantitative metrics**: Tables with exact numbers from paper
- **Qualitative results**: Visual analysis of figures
- **Ablation studies**: Component importance analysis
- **Comparison baselines**: Performance relative to other methods

## Professional Terminology Handling
- **First occurrence**: Provide brief explanation for domain-specific terms
- **LaTeX formatting**: Use `$$` for mathematical equations
- **Variable definitions**: Clearly define all symbols and variables
- **Code references**: Link concepts to specific code files and lines

## Output Format
Generate comprehensive markdown report with:
1. **Structured sections** following the analysis framework
2. **Code snippets** with file paths and line numbers
3. **Mathematical equations** in LaTeX format
4. **Tables** for quantitative comparisons
5. **Critical insights** and personal analysis

## When to Use References
- **references/methodology_patterns.md**: For common architectural patterns
- **references/experiment_analysis.md**: For interpreting results
- **references/code_reading.md**: For systematic code exploration

## Resources

This skill includes example resource directories that demonstrate how to organize different types of bundled resources:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Claude for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Claude's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Claude should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Claude produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.
