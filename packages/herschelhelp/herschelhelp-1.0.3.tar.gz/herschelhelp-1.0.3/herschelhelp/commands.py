# -*- coding: utf-8 -*-

import os

import click
from astropy.io.registry import IORegistryError
from astropy.table import Table
from pymoc import MOC

from .depth_coverage import get_depth_coverage
from .external import convert_table_for_cigale
from .filters import (correct_galactic_extinction, export_to_cigale,
                      export_to_eazy, get_filter_meta_table)
from .footprints import compute_coverages


@click.group()
def cli():
    """Herschel Extra-galactic Legacy Programme tool.

    Execute "herschelhelp <COMMAND> --help" to display the help of a command.
    """
    pass


@cli.command(short_help="Prints % of HELP covered by a MOC")
@click.argument("moc_file", metavar="<moc_file>")
def covbymoc(moc_file):
    """Prints the percentage of HELP covered by a MOC.

    Given a FITS Multi-order coverage map (MOC) footprint, this command
    displays the percentage of each HELP field covered by it.

    <moc_file> must be a FITS file containing a MOC.

    """

    footprint = MOC()
    footprint.read(moc_file)

    coverages = compute_coverages(footprint)

    output = Table(
        data=[list(coverages.keys()), list(coverages.values())],
        names=["Field", "Coverage"]
    )

    print(output)


@cli.command(short_help="Gets the MOC corresponding to depth criteria")
@click.option('--limit', '-l', type=(str, float), multiple=True,
              help="Limit criterion: filter, limit")
@click.option('--output', '-o', default="coverage.fits",
              help="Name of the output FITS file containing the MOC "\
              "(coverage.fits by default).")
def mocfromdepth(limit, output):
    """Produce the MOC corresponding to depth constraints.

    Given a list of bands and maximum error, this command produces
    a Multi-Order Coverage map (MOC) of the corresponding area. The programme
    connects to the HELP Virtual Observatory to get the information.

    Example
    -------
    $ herschelhelp mocfromdetph --limit irac_i1 2 --limit 90prime_g 10

    Will get the area covered by IRAC I1 band and 90Prime g band, with
    a maximum depth of 10 μJy in the former and 10 μJy in the later.

    """
    if os.path.isfile(output):
        raise click.BadOptionUsage("The file {} already exists".format(output))

    if len(limit) == 0:
        raise click.BadParameter("You must provide at least one depth limit. "
                                 "See herschelhelp mocfromdepth --help.")
    else:
        result = get_depth_coverage(dict(limit))
        result.write(output)
        print("The corresponding area was saved to {}. It covers {} square " \
              "degrees.".format(output, result.area_sq_deg))


@cli.command(short_help="Generate CSV file with filter information.")
@click.option('-f', default="help_filters.csv", type=str,
              help="Name of the CSV file (help_filters.csv by default).")
def filter_meta(f):
    """Save filter information to a CSV file.

    This command creates a CSV file containing the information on the various
    filters used in HELP.

    """
    if os.path.isfile(f):
        raise click.BadOptionUsage("The file {} already exists.".format(f))

    filter_table = get_filter_meta_table()
    filter_table.sort('mean_wavelength')
    filter_table.write(f, format='ascii.csv')


@cli.command(short_help="Generate filter files for CIGALE.")
@click.option('-d', default="filters", type=str,
              help="Directory where to store the filter files."
                   " Must not exist.")
def filter_export_cigale(d):
    """Export HELP filters to be used with CIGALE.

    This command export the filters used within HELP to files that can be
    imported in CIGALE for SED fitting.

    """
    if os.path.isdir(d):
        raise click.BadOptionUsage(
            "The directory {} already exists.".format(d))
    if os.path.isfile(d):
        raise click.BadOptionUsage("A file named {} exists".format(d))

    os.mkdir(d)
    export_to_cigale(d)


@cli.command(short_help="Generate filter files for EAZY.")
@click.argument("filename", metavar="<filename>")
def filter_export_eazy(filename):
    """Export HELP filters to be used with EAZY.

    This command export the HELP filters used within HELP to files that can be
    used with EAZY for photometric redshift computation.  It's argument is the
    name of the catalogue file that will be processed by EASY.  It must be in
    the HELP format with the aperture flux and error columns as f_ap_<band>
    and ferr_ap_<band>.

    Three new files will be created based on the filename of this table:
    - <filename>.res containing the responses of the used filters;
    - <filename>.translate associating the table columns to their filter;
    - <filename>.info containing additional information on the filters.

    """
    if os.path.exists("{}.res".format(filename)):
        raise click.BadArgumentUsage(
            "The file {}.res already exists".format(filename))
    if os.path.exists("{}.translate".format(filename)):
        raise click.BadArgumentUsage(
            "The file {}.translate already exists".format(filename))
    if os.path.exists("{}.info".format(filename)):
        raise click.BadArgumentUsage(
            "The file {}.info already exists".format(filename))

    export_to_eazy(filename)


@cli.command(short_help="Correct a catalogue for galactic extinction.")
@click.argument("filename", metavar="<filename>")
def correct_for_extinction(filename):
    """Correct HELP catalogue for galactic extinction.

    This command takes a HELP formatted catalogue and correct its fluxes and
    magnitudes for galactic extinction using the E(B-V) information associated
    with each source.  The catalogue must have an ebv column and the fluxes and
    magnitudes columns are identified using the HELP column format (f_<filter>,
    ferr_filter, f_ap_<filter>, ...).

    Column associated with filters that are not in the HELP database will not
    be corrected and an error message will be logged with the name of the
    missing filters.

    The corrected catalogue will be save as <filename>_corrected.fits.

    """
    new_name = "{}_extcor.fits".format(os.path.splitext(filename)[0])

    if os.path.exists(new_name):
        raise click.UsageError("{} already exists.".format(new_name))

    # TODO: Find a way to deal with not readable ascii files
    try:
        catalogue = Table.read(filename)
    except IORegistryError:
        catalogue = Table.read(filename, format='ascii')

    catalogue = correct_galactic_extinction(catalogue, inplace=True)
    catalogue.write(new_name)


@cli.command(short_help="Convert an HELP catalogue to be processed by CIGALE.")
@click.option("-c", "--cor_ext", is_flag=True,
              help="Correct the catalogue for galactic extinction. The ebv "
              "column must be present.")
@click.option("-z", "--remove_zerofluxes", is_flag=True,
              help="Set flux and error to NaN for fluxes equal to 0.")
@click.argument("filename", metavar="<filename>")
def tocigale(remove_zerofluxes, cor_ext, filename):
    """Convert an HELP catalogue to be processed by CIGALE.

    CIGALE has different requirement for its input catalogues as the standard
    for HELP catalogue.  This command converts a catalogue from HELP to be
    processed by CIGALE:

    - The “help_id” column is renamed to “id”;

    - Only the total flux columns are kept;

    - Only the source with a redhift are kept;

    - The flux and error columns are renamed to <filter> and <filter>_err;

    - The fluxes that are flagged not to be used in SED fitting as set to Nan;

    - The fluxes are converted to mJy.

    - For each source, when a filter bandpass overlaps (or is below) the Lyman
      limit at the source redshift, the flux and error are set to NaN.

    Optionally:

    - The catalogue canremove_zero_fluxes be corrected for galactic extinction;

    - The fluxes which are equals to 0 can be removed as this may indicate an
      upper limit that should be dealt in a more specific way by CIGALE.

    """
    if cor_ext:
        new_name = "{}_cigale_extcor.fits".format(
            os.path.splitext(filename)[0])
    else:
        new_name = "{}_cigale.fits".format(os.path.splitext(filename)[0])

    if os.path.exists(new_name):
        raise click.UsageError("{} already exists.".format(new_name))

    # TODO: Find a way to deal with not readable ascii files
    try:
        catalogue = Table.read(filename)
    except IORegistryError:
        catalogue = Table.read(filename, format='ascii')

    if cor_ext:
        catalogue = correct_galactic_extinction(catalogue, inplace=True)

    catalogue = convert_table_for_cigale(catalogue, inplace=True,
                                         remove_zerofluxes=remove_zerofluxes)
    catalogue.write(new_name)
