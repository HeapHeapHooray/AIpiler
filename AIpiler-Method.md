## Documentation
### 1 Generate first ARCHITECTURE.md   
### 2. Iterate over functions, tagging them and explaining them in ARCHITECTURE.md, answering and asking questions about the overall architecture in QUESTIONS.md.\
   
## Annotations   
### 1. Weight all accumulated function tags into WEIGHTED_TAGS.md, taking into consideration the expertise in ARCHITECTURE.md   
### 2. Rename functions according to weighted tags, taking into consideration the actual code and expertise from ARCHITECTURE.md.   
### 3. Analyze the function names and separate them by subsystem, tagging them with Subsystem_NAME.   
### 4. Annotate globals.   
### 5. Annotate locals.  

## Decompilation
- Uses an intermediate specification/test-driven-development markdown file, which is used as a basis for the output code.
### 1. Generate markdown file.   
### 2. Generate code based on markdown file.   
### 3. Make sure it compiles.   
### 4. Commit.   
### 5. Describe the architecture of the final code in details in FINAL_ARCHITECTURE.md   
### 6. Note the differences of FINAL_ARCHITECTURE.md to the ARCHITECTURE.md file create in the previous stages, in DIFFERENCES.md.   
### 7. Improve markdown file based on differences.   
### 8. Go back to step 2.   
       
