# Copyright (c) 2023 구FS, all rights reserved. Subject to the MIT licence in `licence.md`.
import inspect
import logging
import os
from KFSlog import KFSlog


def force_input(prompt: str, inputs_allowed: list[str]=["y", "n"], tries_max: int=0, match_case_sensitive: bool=False) -> str:
    """
    Forces user to input a string from a list of allowed strings. If case_sensitive is false, input matching is case-insensitive but case of inputs_allowed is returned. If user input is not in inputs_allowed and tries_max has been exhausted, raises ValueError.

    Arguments:
    - prompt: message to (repeatedly) display to user prompting for input
    - input_allowed: list of allowed user input
    - tries_max: maximum number of tries allowed before raising ValueError, 0 for infinite
    - match_case_sensitive: input evaluation case-sensitive or not

    Returns:
    - user_input_normalised: input string from inputs_allowed that user input matched

    Raises:
    - ValueError: user input is not in input_allowed and tries_max has been exhausted
    """

    input_allowed_matched: str  # entry from inputs_allowed that matched user input
    logger: logging.Logger      # logger
    try_current: int=0          # try current
    user_input: str             # user input
    

    if 1<=len(logging.getLogger("").handlers):  # if root logger defined handlers:
        logger=logging.getLogger("")            # also use root logger to match formats defined outside KFS
    else:                                       # if no root logger defined:
        logger=KFSlog.setup_logging("KFS")      # use KFS default format

    if tries_max==0:    # if infinite tries:
        tries_max=-1    # set tries_max to -1 to make while loop run infinitely


    while try_current!=tries_max:   # as long as tries not exhausted: prompt for input
        try_current+=1              # increment try_current
        logger.info(prompt)         # prompt user for input
        user_input=input()          # get user input
        
        if user_input in inputs_allowed:                                                                                                # try to find match case-sensitive and prefer that
            input_allowed_matched=user_input
            break
        elif match_case_sensitive==False and user_input.casefold() in [input_allowed.casefold() for input_allowed in inputs_allowed]:   # if no match case-sensitive found and match case-insensitive allowed: fallback to try to find match case-insensitive
            input_allowed_matched=next(input_allowed for input_allowed in inputs_allowed if input_allowed.casefold()==user_input.casefold())
            break
            
        if try_current!=tries_max:  # if no match and not last try: try again
            logger.warning(f"Input \"{user_input}\" is invalid. Trying again...")
            continue
        else:                       # if no match and last try: error
            logger.error(f"Input \"{user_input}\" is invalid. Giving up.")
            raise ValueError(f"Error in {force_input.__name__}{inspect.signature(force_input)}: Input \"{user_input}\" is invalid. Giving up.")
        
    return input_allowed_matched


def load_config(filepath: str, default_content: str="", empty_ok: bool=False, encoding="utf8") -> str:
    """
    Tries to load text content from \"filepath\" and return it. If file does not exist, tries to create new file with default_content and then raises FileNotFoundError. If file does exist and is empty, may raise ValueError depending on empty_ok.

    Arguments:
    - filepath: filepath to config file to read from or to create
    - defeault_content: if file at filepath does not exist: default config file content to use
    - empty_ok: if config file is empty: return empty string or raise ValueError
    - encoding: encoding to use when reading and writing config file, more at https://docs.python.org/3/library/codecs.html#standard-encodings

    Returns:
    - filecontent: config file content

    Raises:
    - FileNotFoundError: File at filepath does not exist, but has been created and filled with default_content now.
    - IsADirectoryError: File at filepath does not exist, because it is a directory. 
    - ValueError: File at filepath does exist, but empty_ok is false and file is empty.
    """

    filecontent: str
    logger: logging.Logger  # logger
    

    if 1<=len(logging.getLogger("").handlers):  # if root logger defined handlers:
        logger=logging.getLogger("")            # also use root logger to match formats defined outside KFS
    else:                                       # if no root logger defined:
        logger=KFSlog.setup_logging("KFS")      # use KFS default format


    if os.path.isfile(filepath)==False and os.path.isdir(filepath)==False:  # if input configuration file does not exist yet: create a default one, print instructions with error
        logger.error(f"Loading \"{filepath}\" is not possible, because file does not exist.")
        logger.info(f"Creating default \"{filepath}\"...")
        try:
            if os.path.dirname(filepath)!="":
                os.makedirs(os.path.dirname(filepath), exist_ok=True)   # create folders
            with open(filepath, "wt") as file:                          # create file
                file.write(default_content)                             # fill with default content
        except OSError:
            logger.error(f"\rCreating default \"{filepath}\" failed.")
            raise FileNotFoundError(f"Error in {load_config.__name__}{inspect.signature(load_config)}: Loading \"{filepath}\" is not possible, because file does not exist. Creating default \"{filepath}\" failed.")
        else:
            logger.info(f"\rCreated default \"{filepath}\".")
            raise FileNotFoundError(f"Error in {load_config.__name__}{inspect.signature(load_config)}: Loading \"{filepath}\" is not possible, because file did not exist. Created default \"{filepath}\".")
    
    elif os.path.isfile(filepath)==False and os.path.isdir(filepath)==True: # if input configuration file is a directory: can't do anything, error
        logger.error(f"Loading \"{filepath}\" is not possible, because it is a directory. Unable to create default file.")
        raise IsADirectoryError(f"Error in {load_config.__name__}{inspect.signature(load_config)}: Loading \"{filepath}\" is not possible, because it is a directory. Unable to create default file.")


    logger.info(f"Loading \"{filepath}\"...")
    try:
        with open(filepath, "rt", encoding=encoding) as file:   # read file
            filecontent=file.read()
    except OSError:                                             # write to log, then forward exception
        logger.error(f"\rLoading \"{filepath}\" failed with OSError.")
        raise
    else:
        logger.info(f"\rLoaded \"{filepath}\".")
    
    if filecontent=="" and empty_ok==False:                         # but if content is empty and not allowed empty:
        logger.error(f"\rLoaded \"{filepath}\", but it is empty.")  # error
        raise ValueError(f"Error in {load_config.__name__}{inspect.signature(load_config)}: Loaded \"{filepath}\", but it is empty.")
    
    return filecontent