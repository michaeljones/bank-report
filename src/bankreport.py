#!/usr/bin/env python

import sys
import csv
import locale
import textwrap

locale.setlocale(locale.LC_ALL, "")


class Filter( object ):

    pass

class FirstWordFilter( Filter ):

    def __init__( self, word ):

        self.word = word

    def process( self, entry ):

        if entry.from_.startswith( self.word ):
            entry.from_ = self.word

        return entry

class MultiFilter( Filter ):

    def __init__( self, *filters ):

        self.filters = filters

    def process( self, entry ):

        for filter_ in self.filters:
            entry = filter_.process( entry )

        return entry


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

        generator = ( locale.format_string( "\t%s %.2f", ( key, value ), True ) for key, value in items )
        content = "\n".join( generator )

        format = textwrap.dedent( "%3s: %s\n%s" )

        return format % ( self.name, self.total, content )


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

        format = textwrap.dedent( """
        %s

        %s
        """ )

        return locale.format_string( format, ( self.in_, self.out ), True )



class Entry( object ):

    def __init__( self, data ):
        self.type_ = data[0]
        self.from_ = data[1] or "<no name>"
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

    filter_ = MultiFilter(
            FirstWordFilter( "Bnz" ),
            FirstWordFilter( "Nbnz" ),
            )

    filtered_data = ( filter_.process( entry ) for entry in named_data )

    gatherer = Gatherer()

    map( gatherer.gather, filtered_data )

    print gatherer
    

if __name__ == "__main__":
    main( sys.argv )


