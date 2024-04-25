Package Name
==============================================================================

This customization ...

Installation
------------------------------------------------------------------------------

The customization is installed using `Customization Manager`_.  Check out the
instructions for downloading Customization Manager and managing
customizations in the `documentation`_.

.. _Customization Manager: https://customization-manager.readthedocs.io/
.. _documentation: https://customization-manager.readthedocs.io/en/latest/howtos.html

Environment Setup
------------------------------------------------------------------------------

The customization depends on the optional fields being configured in 
Common Services.

The validation list for each optional field is used to validate the data input
into the A/R Receipt Adjustments grid.

These optional fields must also be setup as a Transaction Detail Optional Field
for the G/L Accounts that are used in A/R Receipt Adjustments.

In addition, the customization depends on the Payment Code of the A/R Receipt
Adjustment being written to the G/L Detail Comment field.  This requires that
in :guilabel:`Accounts Receivable --> A/R Setup --> G/L Integration`, on the
:guilabel:`Transactions` tab, the 
:guilabel:`Miscellaneous Adjustment Detail -- G/L Detail Comment` be set to
``Batch Type-Batch Number``

.. image:: images/ar_gl_options_misc_adj_comment.png
    :width: 800px

Custom Table 
------------------------------------------------------------------------------

The customization deploys a custom table that is used to store the optional 
field values. This table should not be manipulated by hand, it is used
to account for the data internally.

Configuration and Usage
-------------------------------------------------------------------------------

The position of the optional field columns in the grid can be changed
by dragging and dropping the columns like any other.

Debugging
-------------------------------------------------------------------------------

Debugging can be enabled for the customization if troubleshooting needs to be
done.  The enable debug:

1. Create an empty file at ``%SHAREDDATA%\COMPANY\<org>\ppadjpro.debug``.
2. Close and re-open the A/R Receipts Screen.

Additional information will be displayed in message boxes and will be saved to
the file ``%SHAREDDATA%\COMPANY\<org>\ppadjpro.log``.

To disable debugging, delete the ``ppadjpro.debug`` file and re-open the 
screen.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
