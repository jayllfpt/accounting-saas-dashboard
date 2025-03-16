# Development Process

This document outlines my process for developing applications using AI assistance. The complete process was shared on [LinkedIn](https://www.linkedin.com/pulse/jayllfptgithubio-ph%E1%BA%A7n-2-implement-ph%E1%BA%A1m-ph%C3%BA-ng%E1%BB%8Dc-trai-mjahf).

## Development Lifecycle

1. Idea Generation
2. Requirements Gathering
3. System Design
4. Code Structure Planning
5. Module Implementation
6. Module Testing
7. Integration
8. Containerization
9. Deployment
10. Maintenance

## Tools used
1. ChatGPT: ChatGPT is awesome for general tasks: summary, analyze, suggestion, planning, etc
2. Cursor AI with Claude 3.7 models: Perfect tools for coding.


## AI Interaction Strategy
I utilize two distinct chatflows when working with ChatGPT:

### Prompt Builder:
- Helps clarify ideas through targeted questions
- Explores project scope and constraints
- Refines prompts for better results

### Generator
- Performs deep analysis of requirements
- Generates detailed, contextual responses
- Provides implementation suggestions

### Quality Control
I carefully review all AI-generated content and selectively incorporate relevant portions into subsequent prompts and tasks. This ensures the output aligns with project requirements while maintaining quality standards.

### My Process for This Assignment

1. Requirements Analysis
- Analyzed requirements from [Requirements](ProjectDocuments/0.%20Requirements)
- Since I was not familiar with accounting operations, I used ChatGPT to analyze the business domain of an Accounting SaaS company and define user stories ([User Story](ProjectDocuments/1.%20User%20Story))

2. Software Requirements Specification
- Based on the user stories, filtered and defined the [SRS](ProjectDocuments/2.%20SRS)

3. Architecture Planning
- Defined [source code structure](ProjectDocuments/3.%20Source%20Code%20Structure) and [implementation plan](ProjectDocuments/4.%20Implementing%20Plan)
- This helped me:
  - Manage modules effectively
  - Use AI to implement each module efficiently
  - Have clear context for implementation through predefined tasks

4. System Design
- Generated system design based on the planned code structure
- Created module diagrams, flow charts, and other visual documentation ([System Diagrams](Mermaids))

5. Implementation
- Due to time constraints, focused on implementing two key features: FR-01 and FR-04
- Followed the design and source code structure using Cursor AI
- Performed bug fixes and refinements

6. Testing
- Conducted product testing through:
  - Manual testing
  - Unit testing
  - Integration testing

7. Documentation
- Created comprehensive project documentation
- Included setup instructions, architecture details, and usage guides
