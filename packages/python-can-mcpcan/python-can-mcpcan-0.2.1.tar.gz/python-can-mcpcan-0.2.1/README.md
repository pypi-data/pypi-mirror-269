## python-can-mcpcan



This module is a plugin that lets you use [MCPcan adapters](available only from d10automation) with the [MCPcan firmware](softmagic) in python-can.


### Installation

Install using pip:

    $ pip install python-can-mcpcan


### Usage

Overall, using this plugin is quite similar to the main Python-CAN library, with the interface named `mcpcan`. For most scenarios, incorporating a MCPcan interface is as easy as modifying Python-can examples with the lines provided below:

Create python-can bus with the mcpcan serial interface:

    import can

    bus = can.Bus(interface="mcpcan", channel="COM2", fd=True, bitrate=500000, data_bitrate=2000000)
