/*
 * virnetserver.h: generic network RPC server
 *
 * Copyright (C) 2006-2015 Red Hat, Inc.
 * Copyright (C) 2006 Daniel P. Berrange
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library.  If not, see
 * <http://www.gnu.org/licenses/>.
 *
 * Author: Daniel P. Berrange <berrange@redhat.com>
 */

#ifndef __VIR_NET_SERVER_H__
# define __VIR_NET_SERVER_H__

# ifdef WITH_GNUTLS
#  include "virnettlscontext.h"
# endif
# include "virnetserverprogram.h"
# include "virnetserverclient.h"
# include "virnetserverservice.h"
# include "virobject.h"
# include "virjson.h"


virNetServerPtr virNetServerNew(const char *name,
                                unsigned long long next_client_id,
                                size_t min_workers,
                                size_t max_workers,
                                size_t priority_workers,
                                size_t max_clients,
                                size_t max_anonymous_clients,
                                int keepaliveInterval,
                                unsigned int keepaliveCount,
                                const char *mdnsGroupName,
                                virNetServerClientPrivNew clientPrivNew,
                                virNetServerClientPrivPreExecRestart clientPrivPreExecRestart,
                                virFreeCallback clientPrivFree,
                                void *clientPrivOpaque);

virNetServerPtr virNetServerNewPostExecRestart(virJSONValuePtr object,
                                               const char *name,
                                               virNetServerClientPrivNew clientPrivNew,
                                               virNetServerClientPrivNewPostExecRestart clientPrivNewPostExecRestart,
                                               virNetServerClientPrivPreExecRestart clientPrivPreExecRestart,
                                               virFreeCallback clientPrivFree,
                                               void *clientPrivOpaque);

void virNetServerClose(virNetServerPtr srv);

virJSONValuePtr virNetServerPreExecRestart(virNetServerPtr srv);

int virNetServerAddService(virNetServerPtr srv,
                           virNetServerServicePtr svc,
                           const char *mdnsEntryName);

int virNetServerAddClient(virNetServerPtr srv,
                          virNetServerClientPtr client);

int virNetServerAddProgram(virNetServerPtr srv,
                           virNetServerProgramPtr prog);

# if WITH_GNUTLS
int virNetServerSetTLSContext(virNetServerPtr srv,
                              virNetTLSContextPtr tls);
# endif

size_t virNetServerTrackPendingAuth(virNetServerPtr srv);
size_t virNetServerTrackCompletedAuth(virNetServerPtr srv);

int virNetServerAddClient(virNetServerPtr srv,
                          virNetServerClientPtr client);
bool virNetServerHasClients(virNetServerPtr srv);
void virNetServerProcessClients(virNetServerPtr srv);

void virNetServerUpdateServices(virNetServerPtr srv, bool enabled);

int virNetServerStart(virNetServerPtr srv);

const char *virNetServerGetName(virNetServerPtr srv);

int virNetServerGetThreadPoolParameters(virNetServerPtr srv,
                                        size_t *minWorkers,
                                        size_t *maxWorkers,
                                        size_t *nWorkers,
                                        size_t *freeWorkers,
                                        size_t *nPrioWorkers,
                                        size_t *jobQueueDepth);

int virNetServerSetThreadPoolParameters(virNetServerPtr srv,
                                        long long int minWorkers,
                                        long long int maxWorkers,
                                        long long int prioWorkers);

unsigned long long virNetServerNextClientID(virNetServerPtr srv);

virNetServerClientPtr virNetServerGetClient(virNetServerPtr srv,
                                            unsigned long long id);

int virNetServerGetClients(virNetServerPtr srv,
                           virNetServerClientPtr **clients);

size_t virNetServerGetMaxClients(virNetServerPtr srv);
size_t virNetServerGetCurrentClients(virNetServerPtr srv);
size_t virNetServerGetMaxUnauthClients(virNetServerPtr srv);
size_t virNetServerGetCurrentUnauthClients(virNetServerPtr srv);

int virNetServerSetClientProcessingControls(virNetServerPtr srv,
                                            long long int maxClients,
                                            long long int maxClientsUnauth);

#endif /* __VIR_NET_SERVER_H__ */
