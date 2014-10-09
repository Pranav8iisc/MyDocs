# Copyright (c) 2001, Stanford University
# All rights reserved.
#
# See the file LICENSE.txt for information on redistributing this software.

import sys

sys.path.append( "../../glapi_parser" )
import apiutil

keys = apiutil.GetDispatchedFunctions("../../glapi_parser/APIspec.txt")

apiutil.CopyrightC()

print """
/* DO NOT EDIT - THIS FILE GENERATED BY THE diffapi.py SCRIPT */
#include "cr_spu.h"
#include "cr_packfunctions.h"
#include "replicatespu.h"
#include "replicatespu_proto.h"

#include <stdio.h>

static const CRPixelPackState defaultPacking = {
	0, 		/* rowLength */
	0, 		/* skipRows */
	0, 		/* skipPixels */
	1, 		/* alignment */
	0, 		/* imageHeight */
	0, 		/* skipImages */
	GL_FALSE, 	/* swapBytes */
	GL_FALSE  	/* psLSBFirst */
};

"""

for func_name in apiutil.AllSpecials( "replicatespu_pixel" ):
	return_type = apiutil.ReturnType(func_name)
	params = apiutil.Parameters(func_name)
	print 'extern %s REPLICATESPU_APIENTRY replicatespu_Diff%s( %s );' % ( return_type, func_name, apiutil.MakeDeclarationString( params ) )

for func_name in apiutil.AllSpecials( "replicatespu_pixel" ):
	return_type = apiutil.ReturnType(func_name)
	params = apiutil.Parameters(func_name)
	print '%s REPLICATESPU_APIENTRY replicatespu_Diff%s( %s )' % (return_type, func_name, apiutil.MakeDeclarationString( params ) )
	print '{'
	params.append( ('&defaultPacking', 'foo', 0) )
	print '\tif (replicate_spu.swap)'
	print '\t{'
	print '\t\tcrPack%sSWAP( %s );' % (func_name, apiutil.MakeCallString( params ) )
	print '\t}'
	print '\telse'
	print '\t{'
	print '\t\tcrPack%s( %s );' % (func_name, apiutil.MakeCallString( params ) )
	print '\t}'
	print '}'

print """
void replicatespuCreateDiffAPI( void )
{
"""

for func_name in keys:
	props = apiutil.Properties(func_name)

	if "get" in props:
		print '\treplicate_spu.diff_dispatch.%s = NULL;' % func_name
	elif apiutil.FindSpecial( "replicatespu_diff", func_name ):
		print '\treplicate_spu.diff_dispatch.%s = crState%s;' % (func_name, func_name)
	elif apiutil.FindSpecial( "replicatespu_pixel", func_name ):
		print '\treplicate_spu.diff_dispatch.%s = replicatespu_Diff%s;' % (func_name, func_name)
	else:
		print '\treplicate_spu.diff_dispatch.%s = (replicate_spu.swap ? crPack%sSWAP : crPack%s);' % (func_name, func_name, func_name)
print '\tcrStateDiffAPI( &replicate_spu.diff_dispatch );'
print '}'