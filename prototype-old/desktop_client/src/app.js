#! /usr/bin/env node

'use strict';
import 'source-map-support/register';
import * as util from 'util';
import * as storeit from './storeit';

global.dump = (obj) =>
{
    console.log(util.inspect(obj, false, null));
};
global.config = new storeit.Config();

new storeit.Client()
    .init();
global.config.save();
