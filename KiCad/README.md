"""
# FlexGrid KiCad Design Files

This folder contains the KiCad project files for the Open Muscle FlexGrid, a high-density, 60-sensor forearm band designed for advanced biometric data collection.

## 📁 Folder Contents

- `FlexGrid.kicad_pro` – KiCad project file  
- `FlexGrid.kicad_sch` – Schematic diagram  
- `FlexGrid.kicad_pcb` – PCB layout  
- `symbols/` – Custom schematic symbols  
- `footprints/` – Custom PCB footprints  
- `3dmodels/` – 3D models for components  
- `gerbers/` – Fabrication-ready Gerber files  
- `bom/` – Bill of Materials (CSV format)

## 🧠 About FlexGrid

FlexGrid is a 15x4 sensor matrix (totaling 60 sensors) integrated into a flexible PCB, utilizing an ESP32-S3 microcontroller for data acquisition and transmission. The design emphasizes:

- Ultra-thin 3mm sensor profile  
- High-density sensor arrangement for detailed muscle activity mapping  
- Compatibility with VR applications and prosthetic control systems  
- Open-source hardware principles for accessibility and collaboration

## 🛠️ Getting Started

1. **Install KiCad**: Ensure you have KiCad version 6.0 or later installed. [Download KiCad](https://www.kicad.org/download/)
2. **Open the Project**:
   - Launch KiCad.
   - Open the `FlexGrid.kicad_pro` file to access the full project.
3. **Explore the Design**:
   - View and edit the schematic in the Schematic Editor.
   - Inspect the PCB layout in the PCB Editor.
   - Utilize the 3D Viewer to visualize the assembled board.

## 🏭 Fabrication Files

The `gerbers/` directory contains all necessary files for PCB fabrication, including:

- Top and bottom copper layers  
- Solder mask layers  
- Silkscreen layers  
- Drill files  

These files are compatible with standard PCB manufacturing services.

## 📄 Bill of Materials

Located in the `bom/` directory, the BOM provides a comprehensive list of components, including:

- Reference designators  
- Component values  
- Footprints  
- Manufacturer part numbers  

This information facilitates component sourcing and assembly.

## 🤝 Contributing

We welcome contributions to improve and expand the FlexGrid project. To contribute:

1. Fork the repository.  
2. Create a new branch for your feature or fix.  
3. Commit your changes with clear messages.  
4. Submit a pull request detailing your modifications.

For major changes or proposals, please open an issue to discuss them first.

"""
