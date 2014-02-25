/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package com.a2i.sim.test;

import com.a2i.sim.CommandLine;
import com.a2i.sim.Speaker;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 *
 * @author atrimble
 */
@Component
public class RemoveListenerCommand implements CommandLine {

    private static final Logger LOG = LoggerFactory.getLogger(RemoveListenerCommand.class);

    @Autowired
    private Speaker speaker;

    @Override
    public String getCommand() {
        return "listener";
    }

    @Override
    public void execute(String... args) {
        if(args.length > 2) {
            String cmd = args[1];
            String name = args[2];

            if(cmd.equalsIgnoreCase("remove")) {
                speaker.removeAllListeners(name);
            }
        }
    }
    
}