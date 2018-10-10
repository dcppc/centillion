import re
import logging
import glob
from mailbox import mbox

logging.basicConfig(level=logging.INFO)

def main():

    for mbox_file in glob.glob('mboxes/*.mbox'):
    
        m = mbox(mbox_file)

        try:
            subgroup_name = re.search('dcppc\+(.*).mbox',mbox_file).group(1)

        except AttributeError:
            subgroup_name = None

        if subgroup_name is None:
            raise Exception("Could not extract subgroup name from file %s"%(mbox_file))
        
        msgs = m.items()
        n_msgs = len(msgs)
    
        logging.info("=============================")
        logging.info("Processing mbox %s with %s messages"%(mbox_file,n_msgs))
    
        for i,msg in msgs:
    
            logging.info("Processing message %02d of %02d"%(i+1, n_msgs))
    
            if msg.is_multipart():
                for part in msg.walk():
                    if part.is_multipart():
                        for subpart in part.walk():
                            if subpart.get_content_type() == 'text/plain':
                                body = subpart.get_payload(decode=True)
                    elif part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True)
            elif msg.get_content_type() == 'text/plain':
                body = msg.get_payload(decode=True)



            logging.info("Spot check: https://dcppc.groups.io/g/%s/message/%d should have title \"%s\""%(
                    subgroup_name,
                    i+1,
                    msg['Subject']
            ))

            #import pdb; pdb.set_trace()
            #if (i+1)==26:
            #    logging.info("We are on i=26 now")
            #    logging.info(msg['From'])
            #    logging.info(msg['To'])
            #    logging.info(msg['Subject'])
            #    logging.info(msg['Date'])
            #    logging.info(body)
    
    
            """
            (Pdb) p msg['From']
            '"Isaac Kohane" <kohane@gmail.com>'
            (Pdb) p msg['Subject']
            'KC3 - Todos before next meeting'
            (Pdb) p msg['Date']
            'Tue, 28 Nov 2017 17:58:34 -0500'
            (Pdb) p msg['To']
            'kc3@dcppc.groups.io'
            (Pdb) msg['Message-ID']
            '<14FB620F7C0C83E6.17399@groups.io>'
            """

if __name__=="__main__":
    main()

