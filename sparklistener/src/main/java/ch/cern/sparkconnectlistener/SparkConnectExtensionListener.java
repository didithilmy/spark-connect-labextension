package ch.cern.sparkconnectlistener;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

import org.apache.spark.SparkConf;
import org.apache.spark.scheduler.SparkListener;
import org.apache.spark.scheduler.SparkListenerJobEnd;
import org.apache.spark.scheduler.SparkListenerJobStart;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Hello world!
 *
 */
public class SparkConnectExtensionListener extends SparkListener {
    private static final Logger log = LoggerFactory.getLogger("SparkConnectExtensionListener");
    private final Map<Integer, String> jobIdToGroupId = new HashMap<>();

    public SparkConnectExtensionListener(SparkConf sparkConf) {
        log.info("SparkConnectExtensionListener initialized!");
    }

    @Override
    public void onJobEnd(SparkListenerJobEnd jobEnd) {
        final int jobId = jobEnd.jobId();
        final String jobGroupId = this.jobIdToGroupId.get(jobId);
        log.info("Job ended, job ID: " + jobId + ", job group ID: " + jobGroupId);
    }

    @Override
    public void onJobStart(SparkListenerJobStart jobStart) {
        final int jobId = jobStart.jobId();
        final String jobGroupId = jobStart.properties().getProperty("spark.jobGroup.id");
        this.jobIdToGroupId.put(jobStart.jobId(), jobGroupId);
        log.info("Job started, job ID: " + jobId + ", job group ID: " + jobGroupId);

        Set<String> keys = jobStart.properties().stringPropertyNames();
        for (String key : keys) {
            log.info(String.format("%s: %s", key, jobStart.properties().getProperty(key)));
        }
    }
}
