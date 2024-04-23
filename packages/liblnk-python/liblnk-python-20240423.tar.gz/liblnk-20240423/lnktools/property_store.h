/*
 * Property store functions
 *
 * Copyright (C) 2009-2024, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#if !defined( _PROPERTY_STORE_H )
#define _PROPERTY_STORE_H

#include <common.h>
#include <file_stream.h>
#include <types.h>

#include "lnktools_libfwps.h"

#if defined( __cplusplus )
extern "C" {
#endif

int property_store_path_string_fprint(
     const system_character_t *file_entry_path,
     size_t file_entry_path_length,
     FILE *notify_stream,
     libcerror_error_t **error );

int property_store_record_fprint(
     const uint8_t *property_set_identifier,
     const system_character_t *property_set_identifier_string,
     libfwps_record_t *property_record,
     FILE *notify_stream,
     libcerror_error_t **error );

int property_store_set_fprint(
     libfwps_set_t *property_set,
     FILE *notify_stream,
     libcerror_error_t **error );

int property_store_fprint(
     libfwps_store_t *property_store,
     FILE *notify_stream,
     libcerror_error_t **error );

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _PROPERTY_STORE_H ) */

