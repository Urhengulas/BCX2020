# zero-emission-factory

<details>
<summary>Table of contents</summary>

- [about](#about)
  - [problem](#problem)
  - [solution](#solution)
    - [data analysis + expert consultation](#data-analysis--expert-consultation)
    - [optimizer](#optimizer)
  - [assumptions](#assumptions)
- [presentation](#presentation)
- [team members](#team-members)
</details>

## about
The **Zero Emission Factory** was the winning project of the **zero emission track** at the [Bosch Connected Experience Hackathon 2020](https://bosch-connected-world.com/hackathon/).

### problem
Factories all over the world produce goods and use A LOT of energy every day and thereby are responsible for a big share of the energy consumption and CO$_2$-production of a country. 

### solution
This project explores the possibility to optimize the production times for the availability of renewable energy.

#### data analysis + expert consultation
Talking to experts from [Bosch.IO](https://bosch.io/) and [EWE](https://www.ewe.de/) we wrapped our heads around the current mode of producing and identified the possibility of production line optimization.
We validated this idea by analyzing provided data _(data unavailable)_ and found out that many production lines have unused times over the course of a week _(see slide 8 in presentation)_.

#### optimizer
Based on that we've build a production time optimizer (frontend [here](./frontend/) and logic [here](./backend/scheduler.py)).

The production optimizer takes 3 inputs: 
* `earliest_start_time` – earliest point in time the production could start
* `deadline`
* `prod_time` – the time span needed for the production
 
Utilizing the [historical data of the availability of green energy](data/renewData.csv) it computes the best point in time to start your production to use the most renewable energy. 

### assumptions
We made following assumptions for this project:
* predictions for renewable energy are available
* production lines have the flexibility to start and stop their production anytime
* factories have capacities to store goods in-between production steps

## presentation
You can find our final presentation [here](./zero_emission_factory_finals.pdf).

## team members
| github handle                                 | responsibility     |
| :-------------------------------------------- | :----------------- |
| [Edimahler](https://github.com/edimahler)     | light controls     |
| [eemmiillyy](https://github.com/eemmiillyy)   | frontend           |
| [Emil9999](https://github.com/Emil9999)       | iot controls       |
| [MarcelCode](https://github.com/MarcelCode)   | data analysis      |
| [peterruppel](https://github.com/peterruppel) | data analysis      |
| [Simonheu](https://github.com/simonheu)       | pitching           |
| [Urhengulas](https://github.com/Urhengulas)   | production planner |
