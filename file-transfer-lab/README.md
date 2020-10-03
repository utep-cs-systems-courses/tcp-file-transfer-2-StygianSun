To run:

1. Open a shell and rename to server, then run fileServer.py
2. Open another shell and rename to client, then run fileClient.py

What It Does:
fileServer.py and fileClient.py work together to transfer the specified files
(testFile.txt, testFile2.txt, testFile3.txt, ghostFile.txt) from the client to
the server. The names and contents of the transferred files are copied to
ServerFiles.txt for verificiation.

Notes:
testFile.txt and testFile2.txt both have contents.
testFile.txt is the first one to be transferred.
testFile2.txt is the third file to be transferred, to test that the system
works after a failed transfer.
ghostFile.txt is a file that doesn't exist in the directory. System should
return a "file not found" error.
testFile3.txt exists in the directory, but has no contents. System should
return a "file empty" error.
