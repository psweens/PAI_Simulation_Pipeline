
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Reconstruction_clean.m
%
% This script performs acoustic wavefield reconstruction using the 
% k-Wave MATLAB toolbox. It reads initial pressure maps generated 
% by SIMPA and runs forward acoustic simulations to reconstruct
% photoacoustic images.
%
% Dependencies:
% - MATLAB
% - k-Wave Toolbox: http://www.k-wave.org/
%
% Usage:
% - Set `inputDir` to the folder containing *_p0.mat pressure maps.
% - Set `outputDir` to the folder for saving reconstructed outputs.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear; close all; clc;

% ------------------- Configuration -------------------
inputDir = 'path/to/optical_sim_output/';       % <- EDIT THIS
outputDir = 'path/to/reconstructed_output/';     % <- EDIT THIS

dx = 0.02e-3;          % voxel spacing in meters
sound_speed = 1500;    % speed of sound in m/s
pml_size = 10;         % perfectly matched layer size

% Create output directory if needed
if ~exist(outputDir, 'dir')
    mkdir(outputDir);
end

% ------------------- Process Each File -------------------
fileList = dir(fullfile(inputDir, '*_p0.mat'));

for k = 1:length(fileList)
    fprintf("Reconstructing: %s\n", fileList(k).name);
    
    % Load initial pressure field
    data = load(fullfile(inputDir, fileList(k).name));
    p0 = data.initial_pressure;
    
    % Ensure correct orientation (SIMPA uses z-y-x, k-Wave expects x-y-z)
    p0 = permute(p0, [3, 2, 1]);

    % Define the computational grid
    [Nx, Ny, Nz] = size(p0);
    kgrid = makeGrid(Nx, dx, Ny, dx, Nz, dx);
    
    % Define medium properties
    medium.sound_speed = sound_speed;
    
    % Define sensor mask (whole volume)
    sensor.mask = ones(Nx, Ny, Nz);
    sensor.record = {'p_final'};
    
    % Define time array
    t_end = 2 * sqrt((Nx*dx)^2 + (Ny*dx)^2 + (Nz*dx)^2) / sound_speed;
    kgrid.t_array = makeTime(kgrid, sound_speed, [], t_end);

    % Simulation settings
    input_args = {...
        'PMLInside', false, ...
        'PMLSize', pml_size, ...
        'DataCast', 'single', ...
        'PlotSim', false ...
    };
    
    % Run the acoustic simulation
    sensor_data = kspaceFirstOrder3D(kgrid, medium, p0, [], sensor, input_args{:});
    
    % Save result
    outputFile = fullfile(outputDir, strrep(fileList(k).name, '_p0.mat', '_recon.mat'));
    save(outputFile, 'sensor_data', '-v7.3');
end

fprintf("All reconstructions complete.\n");
