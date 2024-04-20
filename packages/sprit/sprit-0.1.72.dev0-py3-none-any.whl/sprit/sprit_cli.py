"""This module/script is used to run sprit from the command line. 

The arguments here should correspond to any of the keyword arguments that can be used with sprit.run() (or sprit_hvsr.run()). See the run() function's documentation for more information, or the individual functions that are run within it.

For list inputs, you should pass the argument multiple times(e.g., --report_format "csv" --report_format "print" --report_format "plot"). (In the case of --report_format, you can also just use "all" to get csv, print, and plot report types)

The datapath parameter of input_params() is the only required argument, though for your data processing to work correctly and to be formatted correctly, you may need to pass others as well.
"""

import argparse
import inspect
try:
    import sprit  # When distributed
except:
    import sprit_hvsr as sprit #When testing
    pass

def get_param_docstring(func, param_name):
    function_docstring = func.__doc__

    # Search for the parameter's docstring within the function's docstring
    param_docstring = None
    if function_docstring:
        param_start = function_docstring.find(f'{param_name} :')
        param_start = param_start + len(f'{param_name} :')
        if param_start != -1:
            param_end_line1 = function_docstring.find('\n', param_start + 1)
            param_end = function_docstring.find('\n', param_end_line1 + 1)
            if param_end != -1:
                param_docstring = function_docstring[param_start:param_end].strip()
    
    if param_docstring is None:
        param_docstring = ''
    return param_docstring

def main():
    parser = argparse.ArgumentParser(description='CLI for SPRIT HVSR package (specifically the sprit.run() function)')
    
    hvsrFunctions = [sprit.input_params,
                     sprit.fetch_data,
                     sprit.remove_noise,
                     sprit.generate_ppsds,
                     sprit.process_hvsr,
                     sprit.check_peaks,
                     sprit.get_report,
                     sprit.plot_hvsr]

    #Get default parameters from main functions
    parameters = []
    for f in hvsrFunctions:
        parameters.append(inspect.signature(f).parameters)
    #Add argument and options to the parser
    intermediate_params_list = ['params', 'input', 'hvsr_data', 'hvsr_results']
    paramNamesList = []
    for i, param in enumerate(parameters):
        for name, parameter in param.items():
            # Add arguments and options here
            if name not in paramNamesList and name not in intermediate_params_list:
                paramNamesList.append(name)
                curr_doc_str = get_param_docstring(func=hvsrFunctions[i], param_name=name)
                if name == 'datapath':
                    parser.add_argument(name, help=f'{curr_doc_str}')
                elif name == 'verbose':
                    parser.add_argument('-v', '--verbose',  action='store_true', help='Print status and results to terminal.', default=parameter.default)
                else:
                    helpStr = f'Keyword argument {name} in function sprit.{hvsrFunctions[i].__name__}(). default={parameter.default}.\n\t{curr_doc_str}'
                    parser.add_argument(F'--{name}', help=helpStr, default=parameter.default)
    
    # Add more arguments/options as needed
    args = parser.parse_args()
    
    # Map command-line arguments/options to kwargs
    kwargs = {}
    for arg_name, arg_value in vars(args).items():
        if isinstance(arg_value, str):
            if "=" in arg_value:
                arg_value = {arg_value.split('=')[0]: arg_value.split('=')[1]}

            if arg_value.lower()=='true':
                arg_value = True
            elif arg_value.lower()=='false':
                arg_value = False
            elif arg_value.lower() == 'none':
                arg_value = None
            elif "[" in arg_value:
                arg_value = arg_value.replace('[', '').replace(']','')
                arg_value = arg_value.split(',')
            elif "," in arg_value:
                arg_value = arg_value.split(',')
        kwargs[arg_name] = arg_value
    
    # Call the sprit.run function with the generated kwargs
    kwargs['datapath'] = kwargs['datapath'].replace("'", "") #Remove single quotes to reduce errors
    if str(kwargs['datapath']).lower()=='gui':
        sprit.gui()
    else:
        #Print a summary if not verbose
        if not kwargs['verbose']:
            print("Running sprit.run() with the following arguments (use --verbose for more information):")
            print("sprit.run(", end='')
            for key, value in kwargs.items():
                if 'kwargs' in str(key):
                    pass
                else:
                    if type(value) is str:
                        print(f"{key}='{value}'",end=', ')
                    else:
                        print(f"{key}={value}",end=', ')
            print('**ppsd_kwargs, **kwargs', end='')
            print(')')
    
        sprit.run(**kwargs)
            
if __name__ == '__main__':
    main()