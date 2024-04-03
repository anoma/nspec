# Control Machine

## Purpose
The *Control Machine* aims to centralize the management of configuration settings and measurement data within the
physical machine an Anoma node is running.
It enables dynamic configuration updates,
stores static node configurations,
and records measurements submitted by various engines associated with timestamps.

## Background
In complex distributed systems like Anoma, efficient control and management mechanisms are crucial for ensuring
system stability, scalability, and adaptability.
The *Control Machine* addresses these needs by providing a centralized platform for handling configuration changes and monitoring system performance.

## Scope
For V1, the *Control Machine* encompasses three key engines:
the [Dynamic Configuration Engine](control/dynamic-config.md), the [Static Configuration Engine](control/static-config.md), and the [Measurement Engine](control/measurement.md).
Together, these engines manage dynamic configurations, static configurations, and measurement data, respectively,
providing essential functionality for system control and monitoring.


## Overview
The *Control Machine* is composed of the following three engines.

### [Dynamic Configuration Engine](control/dynamic-config.md#purpose)

--8<-- "control/dynamic-config.md:purpose"

### [Static Configuration Engine](control/static-config.md#purpose)

--8<-- "control/static-config.md:purpose"

### [Measurements Engine](control/measurement.md#purpose)

--8<-- "control/measurement.md:purpose"


## Communication Diagram

![Communication diagram](communication-diagram-control-machine.svg)
