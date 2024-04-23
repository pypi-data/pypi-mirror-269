/*
 * Python object wrapper of liblnk_data_block_t with distributed link tracker properties
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

#if !defined( _PYLNK_DISTRIBUTED_LINK_TRACKING_DATA_BLOCK_H )
#define _PYLNK_DISTRIBUTED_LINK_TRACKING_DATA_BLOCK_H

#include <common.h>
#include <types.h>

#include "pylnk_data_block.h"
#include "pylnk_liblnk.h"
#include "pylnk_python.h"

#if defined( __cplusplus )
extern "C" {
#endif

extern PyMethodDef pylnk_distributed_link_tracking_data_block_object_methods[];
extern PyTypeObject pylnk_distributed_link_tracking_data_block_type_object;

PyObject *pylnk_distributed_link_tracking_data_block_get_machine_identifier(
           pylnk_data_block_t *pylnk_data_block,
           PyObject *arguments );

PyObject *pylnk_distributed_link_tracking_data_block_get_droid_volume_identifier(
           pylnk_data_block_t *pylnk_data_block,
           PyObject *arguments );

PyObject *pylnk_distributed_link_tracking_data_block_get_droid_file_identifier(
           pylnk_data_block_t *pylnk_data_block,
           PyObject *arguments );

PyObject *pylnk_distributed_link_tracking_data_block_get_birth_droid_volume_identifier(
           pylnk_data_block_t *pylnk_data_block,
           PyObject *arguments );

PyObject *pylnk_distributed_link_tracking_data_block_get_birth_droid_file_identifier(
           pylnk_data_block_t *pylnk_data_block,
           PyObject *arguments );

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _PYLNK_DISTRIBUTED_LINK_TRACKING_DATA_BLOCK_H ) */

