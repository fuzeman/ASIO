from asio_windows import WindowsASIO, WindowsInterop

NULL = 0

if __name__ == '__main__':
    file_path = 'test_tmp/test_windows_interop.dat'

    fp = open(file_path, 'w')
    fp.write(file_path)
    fp.close()

    file_handle = WindowsInterop.create_file(
        file_path,
        WindowsASIO.GenericAccess.READ,
        WindowsASIO.ShareMode.ALL,
        WindowsASIO.CreationDisposition.OPEN_EXISTING,
        NULL
    )
    print "file_handle", file_handle

    map_handle = WindowsInterop.create_file_mapping(file_handle, WindowsASIO.Protection.READONLY)
    print "map_handle", map_handle

    view_handle = WindowsInterop.map_view_of_file(map_handle, WindowsASIO.FileMapAccess.READ, 1)
    print "map_view", view_handle

    file_name = WindowsInterop.get_mapped_file_name(view_handle)
    print file_name

    # Close
    WindowsInterop.unmap_view_of_file(view_handle)
    WindowsInterop.close_handle(map_handle)
    WindowsInterop.close_handle(file_handle)
