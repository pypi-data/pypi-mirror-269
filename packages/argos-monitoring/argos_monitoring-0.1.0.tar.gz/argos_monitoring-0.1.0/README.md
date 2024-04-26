# Argos monitoring

A monitoring and status board for your websites.

1. Define a list of websites to monitor
2. Specify a list of checks to run on these websites.
3. Argos will run the checks periodically and alert you if something goes wrong.

Internally, a HTTP API is exposed, and a job queue is used to distribute the checks to the agents.

- [Online documentation](http://framasoft.frama.io/framaspace/argos)
- [Issue tracker](https://framagit.org/framasoft/framaspace/argos/-/issues)

## Requirements

- **Python**: 3.11+
- **Backends**: SQLite (development), PostgreSQL 14+ (production)

## License

Copyright © 2023 Alexis Métaireau, Framasoft

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
[GNU Affero General Public License](LICENSE) for more details.
