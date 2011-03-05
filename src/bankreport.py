#!/usr/bin/env python

import sys
import csv
import locale
import textwrap


class Store( object ):

    def __init__( self, name ):

        self.name = name
        self.total = 0.0
        self.break_down = {}

    def update( self, entry ):

        self.total += entry.amount

        try:
            self.break_down[ entry.from_ ] += entry.amount
        except KeyError:
            self.break_down[ entry.from_ ] = entry.amount

    def __repr__( self ):

        items = sorted( self.break_down.items() )

        return """%3s: %s
        %s
        """ % ( self.name, self.total, "\n".join( "%s %s" % ( key, value ) for key, value in items ) )

class Gatherer( object ):

    def __init__( self ):

        self.in_ = Store( "in" )
        self.out = Store( "out" )

    def gather( self, entry ):

        if entry.amount > 0.0:
            self.in_.update( entry )
        else:
            self.out.update( entry )

    def __repr__( self ):

        locale.setlocale(locale.LC_ALL, "")

        format = textwrap.dedent( """
        %s
        %s
        """ )

        return locale.format_string( format, ( self.in_, self.out ), True )



class Entry( object ):

    def __init__( self, data ):
        self.type_ = data[0]
        self.from_ = data[1]
        self.details = ( data[2], data[3], data[4] )
        self.amount = float(data[5])
        self.date = data[6]

    def __repr__( self ):

        return "%s %s %s %s %s" % ( self.type_, self.from_, self.details, self.amount, self.date )
        

def main(argv):

    filename = argv[1]

    file_ = open( filename )
    lines = ( line for line in file_ )
    csv_data = csv.reader( lines )
    named_data = ( Entry( entry ) for entry in csv_data )

    gatherer = Gatherer()

    map( gatherer.gather, named_data )

    print gatherer
    

if __name__ == "__main__":
    main( sys.argv )

