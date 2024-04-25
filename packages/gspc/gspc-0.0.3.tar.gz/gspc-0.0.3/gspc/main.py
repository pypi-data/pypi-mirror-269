# internal imports
from . import io
from . import core
from .utils.generate_color_gradient import generate_color_gradient as gcg

# external imports
import numpy as np
from tqdm import tqdm
import os
import importlib

def main(settings):
    # Build the output directory
    new_directory = os.path.join(settings.export_directory.get_value(), settings.project_name.get_value())
    
    settings._output_directory = new_directory
    
    # Create the output directory if it does not exist
    if not os.path.exists(settings._output_directory):
        os.makedirs(settings._output_directory)
        
    input_file = settings.path_to_xyz_file.get_value()
    
    # Count the number of configurations in the trajectory
    n_config = io.count_configurations(input_file)
    n_atoms = settings.number_of_atoms.get_value()
    n_header = settings.header.get_value()
    settings.number_of_frames.set_value(n_config)
    
    settings.print_settings()
    
    # Import the extension
    module = importlib.import_module(f"gspc.extensions.{settings.extension.get_value()}")
    
    # Create the box object and append lattice for each frame
    box = core.Box()
    io.read_lattice_properties(box, input_file)
    
    # Create the Cutoff object
    cutoffs = core.Cutoff(settings.cutoffs.get_value())
    
    # Settings the for loop with user settings
    if settings.range_of_frames.get_value() is not None:
        start = settings.range_of_frames.get_value()[0]
        end   = settings.range_of_frames.get_value()[1]
    else:
        start = 0
        end   = n_config
    
    if end-start == 0:
        raise ValueError(f"\tERROR: Range of frames selected is invalid \u279c {settings.range_of_frames.get_value()}.")
    else:
        settings.frames_to_analyse.set_value(end-start)
        
    if settings.quiet.get_value() == False:
        color_gradient = gcg(end-start)
        progress_bar = tqdm(range(start, end), desc="Analysing trajectory ... ", unit="frame", leave=False, colour="YELLOW")
    else:
        progress_bar = range(start, end)
    
    # Keep track of the previous runs if overwrite_results is set to False
    overwrite_results = settings.overwrite_results.get_value()
    
    # Create the results objects
    # TODO complete the list of results objects # PRIO1
    results_pdf = {}
    results_bad = {}
    results_msd = {}
    results_sru = {}
    
    # Generate the keys for the results objects
    keys_pdf = module.return_keys('pair_distribution_function')
    keys_bad = module.return_keys('bond_angular_distribution')
    keys_msd = module.return_keys('mean_square_displacement')
    keys_sru = module.return_keys('structural_units')
    
    # Create the results objects
    for key in keys_pdf:
        results_pdf[key] = io.DistResult("pair_distribution_function", key, start)
        results_pdf[key].write_file_header(settings._output_directory, end-start)
    for key in keys_bad:
        results_bad[key] = io.DistResult("bond_angular_distribution", key, start)
        results_bad[key].write_file_header(settings._output_directory, end-start)
    # for key in keys_msd:
    #     results_msd[key] = io.Result("mean_square_displacement", key, start)
    #     results_msd[key].write_file_header(settings._output_directory, end-start)
    for dict_key in keys_sru:
        for key in dict_key:
            results_sru[key] = io.PropResult(key, dict_key[key], start)
            results_sru[key].write_file_header(settings._output_directory, end-start)
            DEBUG = False    
    # Loop over the frames in the trajectory
    for i in progress_bar:
        # Update the progress bar
        if not settings.quiet.get_value():
            progress_bar.set_description(f"Analysing trajectory n°{i} ... ")
            progress_bar.colour = "#%02x%02x%02x" % color_gradient[i-start]
            
        # Create the System object at the current frame
        if i == start:
            system, reference_positions = io.read_and_create_system(input_file, i, n_atoms+n_header, settings, cutoffs, start, end)
            for atom in system.atoms:
                for ref in reference_positions:
                    if atom.id == ref.id:
                        atom.set_reference_position(ref)
                        # next atom
                        break
        else:
            system, current_positions = io.read_and_create_system(input_file, i, n_atoms+n_header, settings, cutoffs, start, end)
            for atom in system.atoms:
                for cur in current_positions:
                    if atom.id == cur.id:
                        atom.set_current_position(cur)
                        # next atom
                        break
            for atom in system.atoms:
                for ref in reference_positions:
                    if atom.id == ref.id:
                        atom.set_reference_position(ref)
                        # next atom
                        break
        system.frame = i
        
        # Set the Box object to the System object
        system.box = box
        settings.lbox.set_value(system.box.get_box_dimensions(i))
        
        # Calculate the nearest neighbours of all atoms in the system
        system.calculate_neighbours()
        
        # Calculate the mean square displacement
        # system.calculate_mean_square_displacement()
        
        # Calculate the structural units of the system
        system.calculate_structural_units(settings.extension.get_value())
        
        # Calculate the bond angular distribution
        system.calculate_bond_angular_distribution()
        
        # Calculate the pair distribution function
        system.calculate_pair_distribution_function()        
        
        # Add the results to the timeline
        for key in keys_pdf:
            results_pdf[key].add_to_timeline(i, system.distances['r'], system.distances[key])
        for key in keys_bad:
            results_bad[key].add_to_timeline(i, system.angles['theta'], system.angles[key])
        # for key in keys_msd:
        #     results_msd[key].add_to_timeline(i, system.msd[key])
        for d in keys_sru:
            key = list(d.keys())[0]
            sub_keys = d[key]
            results_sru[key].add_to_timeline(i, sub_keys, system.structural_units[key])
        
    for key in keys_pdf:
        results_pdf[key].calculate_average_distribution()
        results_pdf[key].append_results_to_file()
    for key in keys_bad:
        results_bad[key].calculate_average_distribution()
        results_bad[key].append_results_to_file()
    for d in keys_sru:
        key = list(d.keys())[0]
        results_sru[key].calculate_average_proportion()
        results_sru[key].append_results_to_file()
    DEBUG = True