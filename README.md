# NavNirmaan

A unique AI-powered pipeline that transforms standard 2D floor plan images into 3D, walkable Virtual Reality scenes with automated construction cost estimation.

## 🚀 Overview

This project bridges generative AI, parametric modeling, and 3D rendering to create a fully automated pipeline for real estate, architecture, and personal use. 

1. **AI Analysis**: Uses the Gemini Vision model to analyze a 2D floor plan image, extracting parameters like the number of rooms, bedrooms, bathrooms, and total area.
2. **Parametric Generation**: The LLM writes raw OpenSCAD code representing the 3D structure of the house based on the floor plan.
3. **Cost Estimation**: Calculates an estimated construction cost based on the extracted parameters and a specified city.
4. **Procedural Rendering**: Converts the OpenSCAD output to a `.3mf` file, which is then imported headlessly into Blender. A custom Python script assigns procedural PBR materials, generates Nishita sky lighting, and exports a lit, walkable `.blend` (or VR-ready) scene.

## ✨ Features
* **Automated Takeoff**: Extracts room counts and square footage automatically from an image.
* **Cost Estimator**: Built-in logic to estimate construction costs localized to specific cities.
* **Code-Driven 3D Modeling**: Uses OpenSCAD for precise, code-based geometric generation.
* **Headless Blender Pipeline**: Automatically lights and applies materials to the model using Cycles/EEVEE, saving the output as a ready-to-explore `.blend` file.

## 🛠️ Prerequisites

To run this pipeline locally, you will need the following installed on your system:
* **Python 3.8+**
* **Blender** (v3.2 or higher, script optimized for 5.x). Ensure `blender` is accessible in your system's PATH.
* **OpenSCAD**. The script currently uses the flatpak version (`flatpak run org.openscad.OpenSCAD`). If using a native installation, update the command in `Backend/src/Scad.py`.
* **Gemini API Key**: You need an active API key from Google AI Studio.

## ⚙️ Setup & Installation (Docker)

The easiest way to run the entire stack (FastAPI Backend + Frontend Web UI) is via Docker. The provided Dockerfile sets up everything automatically, including Python, Blender, and OpenSCAD.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/DynamicLinker/NavNirmaan.git
   cd NavNirmaan
   ```

2. **Set up your Environment Variables:**
   Create a `.env` file in the root directory of the project and add your Gemini API key:
   ```env
   api_key=YOUR_GEMINI_API_KEY_HERE
   ```

3. **Build the Docker Image:**
   ```bash
   docker build -t navnirmaan .
   ```

## 💻 Usage

1. **Run the Docker Container:**
   Pass your `.env` file into the container when you run it, and map both ports `8000` (Backend) and `8080` (Frontend):
   ```bash
   docker run -p 8000:8000 -p 8080:8080 --env-file .env navnirmaan
   ```

2. **Access the Web App:**
   A basic and simple web UI has been provided to access the main tool. Open your browser and navigate to:
   ```
   http://localhost:8080/
   ```
   
3. **Generate 3D Models:**
   Upload your 2D floor plan through the frontend UI. The FastAPI server (`Backend/server.py`) will automatically process it using the AI model, convert the architecture via OpenSCAD, render the scene headlessly using Blender, and return a `.glb` VR-ready file directly to your browser!

---

## ⚖️ License & Commercial Use

* This software is dual-licensed.

* For Open Source & Non-Commercial Use:
This project is open-source and licensed under the GNU Affero General Public License v3.0 (AGPLv3). You are free to use, modify, and distribute this software for personal, academic, or non-profit applications, provided you adhere to the terms of the AGPLv3 (which includes open-sourcing any derivative works or network services under the same license).

* For Commercial Use:
If you wish to use this software, its API, or its headless rendering pipeline in a commercial product, proprietary SaaS, or closed-source environment without being bound by the AGPLv3 requirement to open-source your own codebase, you must purchase a commercial license.

For commercial licensing inquiries, please contact me directly.


## 🖋️ Attribution Requirement

* If you use this software, fork it, or include any of its core architecture (such as the spatial extraction, OpenSCAD micro-gap logic, or the headless Blender pipeline) in an open-source project or academic research, you must provide explicit attribution.

* You must include the original copyright notices in the source code and credit with a link back to this original GitHub repository.


---

*created by Ajitesh Chaurasia*
